# Deploying Terms of Use versions

Publish the versioned Markdown file to Firebase Storage **before** changing the current version in Realtime Database. Complete the initial setup before shipping an app that requires acceptance; missing configuration or an unreadable file can block access.

This guide documents the configuration in `soft_firebase_backend`. It does not publish or activate a version by itself.

For initial setup, follow steps 1–8. For a later text-only release, follow steps 1 and 4–8; repeat the rules and CORS steps only when those settings change.

## How versioning works

| Item | Location | Publisher |
| --- | --- | --- |
| Required version, as a JSON string | Realtime Database: `/config/termsOfUse/currentVersion` | Administrator through Console or CLI |
| Text for that version | Storage: `legal/terms-of-use/<version>.md` | Administrator through Console or `gcloud` |
| Acceptance history | Realtime Database: `/termsAcceptances/<uid>/<pushId>` | User through the app |

At login, the app checks whether the user has accepted the current version. If not, it downloads the corresponding Markdown and requires acceptance. An acceptance contains `version`, server-stamped `accepted_at`, and optional `email` matching the authenticated user's token.

The rules allow authenticated Storage reads and deny client writes to the legal files. Database reads require an authenticated account present in `/users`; acceptance entries are append-only through the client and must match the current version. Administrative uploads use Google Cloud permissions, not the client's Storage write permissions.

**Published text is final for its version.** Never overwrite or delete a published file, even for a typo: the acceptance history identifies the text by version. Publish a new identifier instead, for example `0.2` after `0.1`. Keep old files and acceptance records.

## Environments and prerequisites

| Environment | Firebase alias | Project ID | Storage bucket |
| --- | --- | --- | --- |
| Development | `dev` | `symbios-core` | `gs://symbios-core.firebasestorage.app` |
| Production | `prod` | `symbios-core-prod` | `gs://symbios-core-prod.firebasestorage.app` |

These mappings come from the backend's `.firebaserc` and README. Recheck them if that configuration changes.

Use a terminal authenticated with Firebase CLI and Google Cloud CLI and an account authorized to deploy rules, upload objects, configure bucket CORS, and update the configuration value. All commands below run from **`C:/workspace/soft_firebase_backend`**, where `firebase.json`, `.firebaserc`, the rules and `storage.cors.json` live.

The main workflow uses **PowerShell**; its variables and commands must not be pasted into cmd or Git Bash. Step 7 also provides a direct activation command tested with **cmd and Git Bash**. In particular, do not use Bash-style single-quote grouping in cmd when passing JSON.

Set the environment and version once, then run the sections in order. For the first development publication, use `dev` and `0.1`. For a subsequent release, use a new version and update the document's version and effective date accordingly.

```powershell
Set-Location 'C:/workspace/soft_firebase_backend'
$termsEnvironment = 'dev'
$termsVersion = '0.1'
$termsSource = 'C:/workspace/symbios-legal/documentos/academico/termos-de-uso.md'
$termsBucket = switch ($termsEnvironment) {
    'dev'  { 'gs://symbios-core.firebasestorage.app' }
    'prod' { 'gs://symbios-core-prod.firebasestorage.app' }
    default { throw 'Choose dev or prod.' }
}
$termsObject = "$termsBucket/legal/terms-of-use/$termsVersion.md"
```

For production, change the environment assignment in this block to `$termsEnvironment = 'prod'` before running it; the bucket follows that selection. Likewise, change `$termsVersion` for each new release. Do not run against emulators when publishing to a live environment. Check that `FIREBASE_DATABASE_EMULATOR_HOST` is not set in the publishing terminal.

## 1. Prepare the text

Review the [Terms source](../documentos/academico/termos-de-uso.md), set its version and effective date, and confirm that the version matches `$termsVersion` exactly. Store the file as UTF-8 Markdown.

Before production, resolve all `[PREENCHER: ...]` and `[VALIDAR: ...]` fields and remove the draft notice. This command helps find them:

```powershell
Select-String -LiteralPath $termsSource -Pattern '\[(PREENCHER|VALIDAR):|MINUTA PARA REVISÃO'
```

Any matches must be resolved before a production upload. Development drafts must also use a new version identifier whenever their published text changes. Once uploaded, a draft is still the permanent text for that version; do not later replace its contents with the final text.

## 2. Deploy rules — initial setup or rule changes

For a project's initial setup, deploy rules before uploading and activating the first version. Repeat this step when the rules change; a text-only release does not require redeploying unchanged rules.

```powershell
firebase deploy --only 'database,storage' --project $termsEnvironment
if ($LASTEXITCODE -ne 0) { throw 'Rules deployment failed. Stop here.' }
```

This deploys the backend's configured Database and Storage rules, including rules for other application data. Review the backend changes being deployed.

## 3. Configure bucket CORS — initial setup or CORS changes

Direct browser downloads from Storage need the bucket's CORS configuration. Inspect and record the existing configuration before changing it:

```powershell
gcloud storage buckets describe $termsBucket --format='default(cors_config)'
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect bucket CORS. Stop here.' }
Get-Content -LiteralPath './storage.cors.json'
```

The backend file currently permits `GET` from all origins, with a 3,600-second preflight cache. Review the file in the current checkout. If the bucket already serves other clients, preserve their required entries in the reviewed configuration before applying it.

**The next command replaces the entire CORS configuration; it does not append entries.** Save the previous CORS array as a separate JSON file if you need to restore it later.

```powershell
gcloud storage buckets update $termsBucket --cors-file=storage.cors.json
if ($LASTEXITCODE -ne 0) { throw 'CORS update failed. Stop here.' }
gcloud storage buckets describe $termsBucket --format='default(cors_config)'
if ($LASTEXITCODE -ne 0) { throw 'Could not verify bucket CORS. Stop here.' }
```

CORS does not grant access to the files; the Storage rules still require authentication. Repeat this step only when CORS needs changing.

The Storage emulator does not implement bucket-level CORS configuration. A passing emulator test cannot validate this step; test an authenticated download from the real application's browser origin. See [Firebase browser-download guidance](https://firebase.google.com/docs/storage/web/download-files) and [emulator limitations](https://firebase.google.com/docs/emulator-suite/connect_storage#bucket-level_metadata).

## 4. Record the previous version

Before publishing, save the current pointer for verification and possible rollback. On a project's first publication it may be `null`.

```powershell
$termsPreviousFile = Join-Path ([System.IO.Path]::GetTempPath()) ('symbios-terms-previous-' + [guid]::NewGuid().ToString('N') + '.json')
firebase database:get /config/termsOfUse/currentVersion --output $termsPreviousFile --project $termsEnvironment
if ($LASTEXITCODE -ne 0) { throw 'Could not read the current version. Stop here.' }
Get-Content -LiteralPath $termsPreviousFile
$termsPreviousVersion = Get-Content -LiteralPath $termsPreviousFile -Raw | ConvertFrom-Json
```

Record the environment and backup-file location with the release. A failed read is not evidence that the value is absent; resolve access or connectivity failures before continuing.

## 5. Upload the new version

Upload the UTF-8 source to the exact object path the app expects:

```powershell
gcloud storage cp $termsSource $termsObject --content-type='text/markdown; charset=utf-8' --if-generation-match=0
if ($LASTEXITCODE -ne 0) { throw 'Upload failed or this version already exists. Do not activate it.' }
```

For `dev` and `0.1`, the destination is `gs://symbios-core.firebasestorage.app/legal/terms-of-use/0.1.md`.

`--if-generation-match=0` rejects the write when a live object already occupies that path, preventing an accidental overwrite. If the version exists, stop and inspect it; use a new version for different text. Do not remove the guard or delete an old object to reuse its version. See [Cloud Storage preconditions](https://docs.cloud.google.com/storage/docs/request-preconditions#the_0_value_in_a_generation-match_precondition).

## 6. Verify the uploaded file before activation

Inspect metadata, download the object and compare its bytes with the source:

```powershell
gcloud storage objects describe $termsObject
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect the uploaded object. Stop here.' }
$termsDownloadedFile = Join-Path ([System.IO.Path]::GetTempPath()) ('symbios-terms-download-' + [guid]::NewGuid().ToString('N') + '.md')
gcloud storage cp $termsObject $termsDownloadedFile
if ($LASTEXITCODE -ne 0) { throw 'Could not download the uploaded object. Stop here.' }
$termsSourceHash = (Get-FileHash -LiteralPath $termsSource -Algorithm SHA256).Hash
$termsUploadedHash = (Get-FileHash -LiteralPath $termsDownloadedFile -Algorithm SHA256).Hash
if ($termsSourceHash -ne $termsUploadedHash) { throw 'Uploaded text differs from the source. Do not activate it.' }
```

Confirm that the content type is `text/markdown; charset=utf-8`, the file is nonempty, accents display correctly, and the text's version/date are the intended release. Keep the source commit and SHA-256 hash with the release record.

An administrative `gcloud` download proves object access for that account; it does not prove the app's Firebase rules or browser CORS behavior. Where possible, verify the exact object through an authenticated app download before activation; complete the login test immediately afterward.

## 7. Activate the version — last publishing step

Write only `/config/termsOfUse/currentVersion`, as a **JSON string**, not a number or an object. Do not replace its parent `/config` or `/config/termsOfUse`.

Choose the command for your shell. If an earlier activation failed but the rules, CORS and file are already in place, correct this write and verify it; there is no need to repeat the upload or redeploy rules just to fix malformed JSON.

### 7.1. cmd or Git Bash

From `soft_firebase_backend`, after verifying the uploaded file, activate the initial dev version with:

```bat
firebase database:set /config/termsOfUse/currentVersion --data "\"0.1\"" --project dev
```

Copy the escaping exactly: **one backslash before each inner double quote**. This passes the valid JSON string `"0.1"` to the CLI. For another release, replace `0.1`; for production, select `prod` only after verifying that version's production file.

Do not use `--data '\"0.1\"'` or the Bash-only form `--data '"0.1"'` in cmd. Single quotes do not group arguments there. With the Bash-only form, the CLI receives `'0.1'`, including apostrophes, which is not valid JSON. The write fails with `400 Invalid data` and the current pointer remains unchanged. If it was missing, the app continues to show “Versão atual dos Termos de Uso não configurada.”.

After a successful write, check the saved value:

```bat
firebase database:get /config/termsOfUse/currentVersion --project dev
```

The JSON output must be **`"0.1"`, including double quotes**. The number `0.1` without quotes is not a valid version value for the app. Do not continue the rollout until the value and type are correct.

### 7.2. PowerShell

Use a JSON file to avoid native-command quote handling changing the value. This example uses the variables from the setup block:

```powershell
$termsVersionFile = Join-Path ([System.IO.Path]::GetTempPath()) ('symbios-terms-version-' + [guid]::NewGuid().ToString('N') + '.json')
ConvertTo-Json -InputObject $termsVersion -Compress | Set-Content -LiteralPath $termsVersionFile -Encoding ascii
Get-Content -LiteralPath $termsVersionFile
firebase database:set /config/termsOfUse/currentVersion $termsVersionFile --project $termsEnvironment
if ($LASTEXITCODE -ne 0) { throw 'Activation failed. Check the pointer before retrying.' }
$termsReadbackFile = Join-Path ([System.IO.Path]::GetTempPath()) ('symbios-terms-readback-' + [guid]::NewGuid().ToString('N') + '.json')
firebase database:get /config/termsOfUse/currentVersion --output $termsReadbackFile --project $termsEnvironment
if ($LASTEXITCODE -ne 0) { throw 'Could not verify activation.' }
Get-Content -LiteralPath $termsReadbackFile
$termsReadbackVersion = Get-Content -LiteralPath $termsReadbackFile -Raw | ConvertFrom-Json
if ($termsReadbackVersion -isnot [string] -or $termsReadbackVersion -cne $termsVersion) {
    throw 'The current version is not the expected string. Do not continue the rollout.'
}
```

For `0.1`, both the JSON file and readback must contain `"0.1"`, including the JSON string quotes. Firebase CLI asks for confirmation before replacing this value; confirm the displayed project and path.

### 7.3. Required readback

| JSON output for the initial release | Meaning | Action |
| --- | --- | --- |
| `"0.1"` | String with the expected version | Continue to the app test. |
| `0.1` | Number | Rewrite it as a JSON string. |
| `null` | No current version configured | Complete the write successfully and check again. |
| Another value or a failed read | Wrong version, environment, type or an access/connectivity issue | Resolve it and read back the correct string before continuing. |

After activation, users without an acceptance for this exact version will be prompted at their next login. Coordinate activation with the document's effective date and the app rollout. For the first release, activate and verify the configuration before shipping the app.

## 8. Verify the app flow

Using the real target environment and a registered, authenticated test user:

1. Log in without an acceptance for the new version and confirm that the correct text loads with no permission, download or CORS errors.
2. Confirm that the app requires acceptance before proceeding.
3. Accept and verify a new entry under `/termsAcceptances/<uid>/<pushId>` with the current string version and a server timestamp. If present, `email` must match the authenticated account.
4. Log in again and confirm the same version is not requested again.
5. Keep the previous files and acceptance entries intact. Do not manually create acceptance records to bypass the flow.

The backend also provides rule tests. From `soft_firebase_backend`, start the emulators in one terminal:

```powershell
firebase emulators:start --only 'database,storage' --project dev
```

With the backend test dependencies installed, run in a second terminal from the same directory:

```powershell
node ./tests/terms-of-use.test.js
```

These tests exercise rules and acceptance records, not live bucket CORS or the complete browser UI. This guide was checked against the backend configuration and CLI interfaces. Inline JSON quoting was tested locally in cmd and Git Bash using an argument probe; no live deployment or browser-CORS test was performed while writing it.

## Subsequent versions and production

For a text-only update, repeat preparation and steps 4–8 with a new version such as `0.2`. Deploy rules or change CORS only if needed. Always upload and verify before switching the pointer.

Validate the release in dev, then select `prod` and publish the same finalized text to the production bucket before changing the production pointer. The environments have independent files, configuration and acceptance histories. Do not promote dev acceptance records to production.

## Rollback and troubleshooting

If activation causes a problem, restore the previous **verified, readable** version pointer in the same environment. First confirm that `$termsPreviousVersion` is a nonempty string and that its object still exists:

```powershell
if ($termsPreviousVersion -isnot [string] -or [string]::IsNullOrWhiteSpace($termsPreviousVersion)) {
    throw 'No previous published version is available for rollback.'
}
gcloud storage objects describe "$termsBucket/legal/terms-of-use/$termsPreviousVersion.md"
if ($LASTEXITCODE -ne 0) { throw 'Previous version file is unavailable. Do not roll back to it.' }
firebase database:set /config/termsOfUse/currentVersion $termsPreviousFile --project $termsEnvironment
if ($LASTEXITCODE -ne 0) { throw 'Rollback failed. Check the current pointer.' }
firebase database:get /config/termsOfUse/currentVersion --project $termsEnvironment
```

The backup file must be the one recorded for this environment and release. Rollback changes only the required version; it does not edit either text or erase acceptances. A user who accepted only the withdrawn version may need to accept the restored one. For a first publication with no previous version, repair the configuration/access issue or publish a corrected new version instead of setting the pointer to `null`.

| Symptom | Check |
| --- | --- |
| Missing file or wrong text | Exact string in `currentVersion`, matching `<version>.md`, bucket and environment. |
| Upload returns precondition failure | The version already exists. Compare it and choose a new identifier for changed text. |
| `400 Invalid data` during `database:set` | Malformed JSON, often caused by using Bash single quotes in cmd or adding extra backslashes. Use the shell-specific command in step 7 and verify the readback. The failed write does not create the missing pointer or replace a prior value. |
| “Versão atual dos Termos de Uso não configurada.” | Read `/config/termsOfUse/currentVersion` in the correct project. If it is `null`, the write has not populated the value. Set the verified uploaded version as a string, then read it back. |
| Pointer is numeric, such as `0.1` | Rewrite the leaf with a JSON string using step 7. |
| `permission_denied` in the app | Check authentication, presence of the user's `/users` record for Database access, and deployed rules. A CLI `400 Invalid data` is a payload error; it does not establish whether the client's rules are deployed, since administrative CLI access differs from client access. |
| Works in emulator but browser download fails | Live bucket CORS and actual browser origin; admin download success does not validate these. |
| Acceptance rejected | Current string version, server timestamp, matching email if supplied, and creation of a new push entry rather than editing an old one. |
| Other clients fail after CORS update | Compare with the saved previous CORS array; restore its reviewed entries and verify all affected clients. |

## References

- Backend implementation: `soft_firebase_backend/README.md`, `.firebaserc`, `firebase.json`, `storage.cors.json`, `storage.rules`, `database.rules.json` and `tests/terms-of-use.test.js`.
- [Firebase CLI — Database commands](https://firebase.google.com/docs/cli#realtime_database_commands).
- [Microsoft cmd — command syntax and quotation marks](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd).
- [Cloud Storage CLI — copying objects](https://docs.cloud.google.com/sdk/gcloud/reference/storage/cp) and [updating bucket CORS](https://docs.cloud.google.com/sdk/gcloud/reference/storage/buckets/update).
