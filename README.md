# Legal Templates

Attorney-drafted legal templates for startups and technology companies. Created by the attorneys at [General Legal](https://general.legal) and released under [CC0 1.0](LICENSE). Free for anyone to use, modify, and distribute for any purpose, without attribution.

These templates are provided in LLM-optimized markdown and original .docx formats. Highlighted text (marked with `<mark>` tags in the markdown files) indicates fields that should be customized for your use.

## Templates

| Template | Description |
|----------|-------------|
| [Business Associate Agreement (BAA)](templates/business-associate-agreement/) | HIPAA-required contract between covered entities and business associates that handle protected health information |
| [Mutual Non-Disclosure Agreement](templates/mutual-nda/) | Two-way confidentiality agreement for parties sharing sensitive information while exploring a business relationship |
| [One-Way Non-Disclosure Agreement](templates/one-way-nda/) | One-way confidentiality agreement protecting a single disclosing party's information |
| [Cookie Notice](templates/cookie-notice/) | Disclosure of cookie and tracking technology practices for websites and apps |
| [Privacy Policy (U.S. Only)](templates/privacy-policy-us/) | Privacy policy covering U.S. federal and state privacy laws including CCPA/CPRA |
| [Privacy Policy (GDPR Enhanced)](templates/privacy-policy-gdpr/) | Multi-jurisdictional privacy policy covering both U.S. state laws and GDPR/UK GDPR |
| [Terms of Use](templates/terms-of-use/) | Website terms of use covering access rights, IP protections, liability limits, and dispute resolution |

## Repository Structure

```
legal-templates/
  templates/                  # One directory per template
    business-associate-agreement/
      README.md               # Template overview, use cases, and key provisions
      template.md             # Full template text in LLM-optimized markdown
    mutual-nda/
    one-way-nda/
    cookie-notice/
    privacy-policy-us/
    privacy-policy-gdpr/
    terms-of-use/
  docx-originals/             # Original .docx source files
  scripts/
    convert_docx.py           # Python script used to convert .docx to markdown
  LICENSE                     # CC0 1.0 Universal
```

