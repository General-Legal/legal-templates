# Legal Templates

Attorney-drafted legal templates for startups and technology companies. Created by the attorneys at [General Legal](https://general.legal) and released under [CC0 1.0](LICENSE). Free for anyone to use, modify, and distribute for any purpose, without attribution.

These templates are provided in LLM-optimized markdown and original .docx formats. Highlighted text (marked with `<mark>` tags in the markdown files) indicates fields that should be customized for your use.

## Scope and Limitations

**Jurisdiction.** These templates are drafted for U.S. companies. Governing law defaults to Delaware, the offer letter is written for California exempt employees, and the privacy documents are built around U.S. federal and state law. The GDPR-enhanced privacy policy and the global DPA add EU/EEA, UK, and Swiss obligations, but no template in this repository is a substitute for local counsel outside the United States — a Canadian, EU, or UK company will need material changes, not just a search-and-replace of the party names.

**Commercial terms are left blank on purpose.** Fees, liability caps, term lengths, and notice periods appear as `<mark>` fields. A template can tell you which clauses belong in an agreement; it cannot tell you which ones you should have negotiated.

**Templates describe your business, not the reverse.** A privacy policy or DPA copied without edits will describe data flows you do not have and omit the ones you do. Read each document against what your product actually does before you publish or sign it.

**Not legal advice.** These templates are provided as-is under CC0. Using them does not create an attorney-client relationship with General Legal or any of its attorneys. Have a lawyer review anything you intend to sign or publish.

## Feedback and Contributions

Found a typo, a stale citation, or a clause that does not fit? Open an [issue](https://github.com/General-Legal/legal-templates/issues) or a pull request — see [CONTRIBUTING.md](CONTRIBUTING.md). Corrections and new templates are both welcome.

## Templates

| Template | Description |
|----------|-------------|
| [Advisor Agreement](templates/advisor-agreement/) | Advisor agreement covering advisory services, equity compensation, IP assignment, and confidentiality |
| [Business Associate Agreement (BAA)](templates/business-associate-agreement/) | HIPAA-required contract between covered entities and business associates that handle protected health information |
| [Cookie Notice](templates/cookie-notice/) | Disclosure of cookie and tracking technology practices for websites and apps |
| [Data Processing Addendum (U.S.)](templates/dpa-us/) | Processor-friendly DPA for U.S. personal data with security measures and state-privacy-law compliance |
| [Data Processing Addendum (Global)](templates/dpa-global/) | Processor-friendly DPA for U.S., EU/EEA, UK, and Switzerland with GDPR-aligned obligations |
| [Employee Offer Letter (California Exempt)](templates/employee-offer-letter/) | Offer letter for California exempt hires covering compensation, exempt-employee policies, and arbitration |
| [Master Services Agreement (MSA)](templates/master-services-agreement/) | Tech-oriented MSA for companies deploying software and providing platform or integration services |
| [Mutual Non-Disclosure Agreement](templates/mutual-nda/) | Two-way confidentiality agreement for parties sharing sensitive information while exploring a business relationship |
| [One-Way Non-Disclosure Agreement](templates/one-way-nda/) | One-way confidentiality agreement protecting a single disclosing party's information |
| [Privacy Policy (U.S. Only)](templates/privacy-policy-us/) | Privacy policy covering U.S. federal and state privacy laws including CCPA/CPRA |
| [Privacy Policy (GDPR Enhanced)](templates/privacy-policy-gdpr/) | Multi-jurisdictional privacy policy covering both U.S. state laws and GDPR/UK GDPR |
| [Terms of Use](templates/terms-of-use/) | Website terms of use covering access rights, IP protections, liability limits, and dispute resolution |

## Repository Structure

```
legal-templates/
  templates/                  # One directory per template
    advisor-agreement/
    business-associate-agreement/
      README.md               # Template overview, use cases, and key provisions
      template.md             # Full template text in LLM-optimized markdown
    cookie-notice/
    dpa-global/
    dpa-us/
    employee-offer-letter/
    master-services-agreement/
    mutual-nda/
    one-way-nda/
    privacy-policy-gdpr/
    privacy-policy-us/
    terms-of-use/
  docx-originals/             # Original .docx source files
  scripts/
    fetch_templates.py        # Downloads .docx files from general.legal/resources/library
    convert_docx.py           # Converts .docx originals to markdown
  LICENSE                     # CC0 1.0 Universal
```

