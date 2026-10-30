# Terms of Use: deploying and updating

How to put the Terms of Use live in OmniRehab, and how to publish a new version later.

- **First deployment:** once per environment (dev, then prod). See [First deployment](#first-deployment).
- **Every new text:** see [Publishing a version](#publishing-a-version). The first deployment uses the same steps for version `0.1`.

> **Replace `X.Y` in every command.** `X.Y` stands for the version you're publishing, for example `0.1` for the first one, then `0.2`, `0.3`, `1.0`. It appears in the file name (`X.Y.md`), in the quoted value (`"\"X.Y\""`) and in the header of the text (`**Versão:** X.Y`), and all three must match exactly. Use a new number for every text you publish.

## How it works

| What | Where | Who writes it |
| --- | --- | --- |
| Current version | Realtime Database: `config/termsOfUse/currentVersion`, a text value such as `"0.1"` | You, through the Console or CLI |
| Text of each version | Storage: `legal/terms-of-use/X.Y.md`, Markdown in UTF-8 | You, through the Console or `gcloud` |
| Acceptance log | Realtime Database: `termsAcceptances/<uid>/<pushId>` = `{ version, accepted_at, email }` | The user, through the app |

At every login the app reads the current version and the user's acceptance log:

- **The user already accepted this version:** the app opens normally.
- **The user accepted an earlier version:** a modal titled **"Termos de Uso atualizados"** shows the new text.
- **The user never accepted:** a modal titled **"Termos de Uso"** shows the text.

The user can't use the app until they accept; **Sair** signs them out. Each acceptance adds an entry to the log with the version, the server's time and the user's e-mail. Entries can't be edited or deleted from the app.

If the app can't read the current version or download its file, nobody can get in: users see "Não foi possível carregar os Termos de Uso". That's why the file always goes up **before** the version is switched.

**Never change a published file.** Acceptances point to the text by its version, so the file behind `0.1` must stay exactly as users accepted it. To fix anything, even a typo, publish a new version. A version has no spaces or `/`, and it is always stored as text.

## Before you start

**Where to run the commands.** Use **cmd or Git Bash**. They don't work as-is in Windows PowerShell, which handles the quotes in step 4 differently.

- **Publishing a version:** open the terminal in the root folder of this repository, `symbios-legal` (the folder with `README.md`, `docs` and `documentos`). One way: open the folder in Explorer, type `cmd` in the address bar and press Enter. Or run `cd /d <path to your symbios-legal folder>` in cmd. The commands use paths relative to that folder, such as `documentos/academico/termos-de-uso.md`.
- **First deployment, steps 1 and 2:** these use files from the backend repository, so run them in the root folder of your `soft_firebase_backend` clone (the one with `firebase.json`, `storage.rules` and `storage.cors.json`).

**Environments.** The examples use **dev**. For production, replace `symbios-core` with `symbios-core-prod` in the commands; that one change covers both `--project` and the bucket name.

| Environment | Project ID (`--project`) | Bucket |
| --- | --- | --- |
| Development | `symbios-core` | `gs://symbios-core.firebasestorage.app` |
| Production | `symbios-core-prod` | `gs://symbios-core-prod.firebasestorage.app` |

**Accounts.** Both CLIs must be logged in with an account that has access to the project. Check with `firebase login:list` and `gcloud auth list`. To switch, run `firebase login:add` then `firebase login:use <account>`, and `gcloud auth login`. A personal account without access gets `403` or `Failed to get details for project`.

## First deployment

Do this once per environment, before releasing an app version that asks for the Terms. If the app ships first, every user is blocked until these steps are done.

Run steps 1 and 2 in the root folder of `soft_firebase_backend`.

### 1. Deploy the rules

```bat
firebase deploy --only database,storage --project symbios-core
```

This replaces **all** Realtime Database and Storage rules of the project with the files in that folder, not just the Terms rules. Deploy from an up-to-date branch that includes the Terms rules. Repeat this step only when the rules change.

### 2. Allow the app to download the text (bucket CORS)

The app downloads the file straight from Storage, which the bucket has to allow. First check whether it already has a CORS configuration:

```bat
gcloud storage buckets describe gs://symbios-core.firebasestorage.app --format="default(cors_config)"
```

If nothing is printed, apply the configuration from the backend:

```bat
gcloud storage buckets update gs://symbios-core.firebasestorage.app --cors-file=storage.cors.json
```

This **replaces** the bucket's CORS configuration. If the first command printed an existing configuration, add its entries to `storage.cors.json` before applying. CORS doesn't make the files public: the Storage rules still require a signed-in user. Repeat this step only when CORS changes.

### 3. Publish version 0.1

Go back to the `symbios-legal` folder and follow [Publishing a version](#publishing-a-version) with `X.Y` = `0.1`. After step 6 passes, the environment is ready for the app release.

## Publishing a version

Use these steps for the first version and for every update. Run them in the root folder of `symbios-legal`, and replace `X.Y` with your version in every command.

### 1. Prepare the text

1. Edit [`documentos/academico/termos-de-uso.md`](../documentos/academico/termos-de-uso.md) and set the header to the new version: `**Versão:** X.Y · ...`.
2. Before production, resolve every `[PREENCHER: ...]` and `[VALIDAR: ...]` field and remove the "MINUTA" notice. This command lists any that are left; it should print nothing:

   ```bat
   findstr /n /l /c:"[PREENCHER" /c:"[VALIDAR" /c:"MINUTA" documentos\academico\termos-de-uso.md
   ```

   In Git Bash:

   ```sh
   grep -nE "\[(PREENCHER|VALIDAR):|MINUTA" documentos/academico/termos-de-uso.md
   ```

3. Commit the text in this repository, so you can always tell which text became which version.

### 2. Upload the file

```bat
gcloud storage cp documentos/academico/termos-de-uso.md gs://symbios-core.firebasestorage.app/legal/terms-of-use/X.Y.md --content-type="text/markdown; charset=utf-8" --if-generation-match=0
```

`--if-generation-match=0` makes the upload fail if `X.Y.md` already exists, so a published version can't be replaced by accident. If it fails with `412 Precondition Failed`, that version is taken: pick a new one and change the header too.

Using the Console instead: in Storage, open the `legal/terms-of-use` folder (create it the first time) and upload a copy of the file renamed to `X.Y.md`.

### 3. Check the upload

```bat
gcloud storage ls -l gs://symbios-core.firebasestorage.app/legal/terms-of-use/
```

The listing should include `X.Y.md` with a size above zero, next to the earlier versions.

### 4. Switch the current version

Do this last. From now on, everyone who hasn't accepted `X.Y` is asked at their next login.

```bat
firebase database:set /config/termsOfUse/currentVersion --data "\"X.Y\"" --project symbios-core
```

Confirm with `y` when the CLI asks. Copy the quoting exactly and replace only `X.Y`: `"\"X.Y\""` sends the text `"X.Y"`. Bash-style single quotes (`'"X.Y"'`) fail in cmd with `400 Invalid data`, and then nothing is saved.

Using the Console instead: in Realtime Database, set `config` → `termsOfUse` → `currentVersion` to `"X.Y"`, **typing the quotes**. Without them the Console saves a number, and the app rejects numbers.

### 5. Read it back

```bat
firebase database:get /config/termsOfUse/currentVersion --project symbios-core
```

| Output | Meaning |
| --- | --- |
| `"X.Y"`, with quotes | Correct: text with the new version. |
| `X.Y`, without quotes | Saved as a number. Redo step 4. |
| `null` | Nothing saved. Redo step 4 and check its output for errors. |

### 6. Test in the app

1. Log in with a test user. If they had accepted an earlier version, the modal says **"Termos de Uso atualizados"**; otherwise **"Termos de Uso"**. Check that "Versão X.Y" and the new text appear.
2. Tick the checkbox and accept. The app opens.
3. In the Realtime Database console, `termsAcceptances/<user uid>` has a new entry with `version: "X.Y"`.
4. Sign out and back in. The modal doesn't show again.

### 7. Production

Repeat steps 2 to 6 with `symbios-core-prod` in place of `symbios-core`, using the same committed text. Dev and prod are independent: each has its own files, current version and acceptance log.

When you switch the version, plan for when users will see it. The Terms (section 10.1) say material changes are announced by e-mail or a prominent notice in the system. The "Termos de Uso atualizados" modal is that notice inside the app; an e-mail is up to you.

## Rolling back

To go back to the previous version, run [step 4](#4-switch-the-current-version) with the previous version in place of `X.Y`, then check it with step 5. Its file is still in Storage, so nothing else is needed. Acceptances are kept. Users who never accepted that earlier version, such as people who joined after the update, will be asked to accept it.

Never delete `currentVersion` or set it to `null`: that blocks everyone.

## Troubleshooting

When the app shows "Não foi possível carregar os Termos de Uso", the cause is logged right after `Erro ao carregar os Termos de Uso:`. Look in DevTools (`Ctrl+Shift+I` in the app) or, in development, in the terminal running `npm run dev`, prefixed with `[browser]`.

| Error in the app log | Cause | Fix |
| --- | --- | --- |
| `permission_denied` | Database rules not deployed, or the user has no record in `/users` | First deployment, step 1 |
| `Versão atual dos Termos de Uso não configurada.` | `currentVersion` is missing or is a number | Publishing, steps 4 and 5 |
| `storage/object-not-found` | No file named `X.Y.md` for the current version | Publishing, steps 2 and 3 |
| `storage/unauthorized` | Storage rules not deployed | First deployment, step 1 |
| `blocked by CORS policy` in DevTools, or `storage/retry-limit-exceeded` | Bucket CORS not set | First deployment, step 2 |

| Error in the terminal | Cause | Fix |
| --- | --- | --- |
| `400 Invalid data; couldn't parse JSON` on `database:set` | Quotes mangled by the shell | Use the exact command from step 4, or the Console with quotes |
| `412 Precondition Failed` on upload | That version already exists | Publish under a new version |
| `403 ... does not have storage...` or `Failed to get details for project` | Logged in with an account without access | See [Before you start](#before-you-start) |
| `The following URLs matched no objects or files: documentos/...` on upload | Terminal not open in the `symbios-legal` folder | See [Before you start](#before-you-start) |

If accepting fails with "Não foi possível registrar seu aceite", the user lost connection, or the version changed while the modal was open. Signing out and back in loads the current version.

## Reference

- App (`soft_omnirehab_web`): `lib/termsOfUse.ts` reads the version, downloads the text and records acceptances; `app/components/TermsOfUseGate.tsx` and `TermsOfUseModal.tsx` handle the screen.
- Backend (`soft_firebase_backend`): `database.rules.json` (`config/termsOfUse`, `termsAcceptances`), `storage.rules` (`legal/terms-of-use`), `storage.cors.json`. `tests/terms-of-use.test.js` checks the rules on the emulators: in that folder, run `firebase emulators:start --only database,storage`, then `node tests/terms-of-use.test.js` in a second terminal.
