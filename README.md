# Symbios — documentos jurídicos da versão acadêmica

Minutas em português, adaptadas para o contexto brasileiro a partir dos modelos General Legal (CC0).

- [Termos de Uso Acadêmico](documentos/academico/termos-de-uso.md)
- [Política de Privacidade e Proteção de Dados](documentos/academico/politica-de-privacidade.md)
- [Acordo de Tratamento de Dados — DPA](documentos/academico/acordo-de-tratamento-de-dados.md)
- [Resumo, premissas e pendências](documentos/academico/README.md)
- [Comparação de modelos e fontes jurídicas](documentos/academico/fontes-e-modelos.md)

**Status: versão 0.1, de 29/10/2026, para revisão.** Os campos `[PREENCHER: ...]` e `[VALIDAR: ...]` precisam ser resolvidos antes da publicação ou assinatura. As minutas consideram dados reais de pacientes, nuvem como armazenamento padrão, armazenamento local temporário e acesso pela Symbios. Melhorias e treinamentos somente podem usar dados efetivamente anonimizados, nas condições descritas nos documentos.

Os modelos originais e sua licença estão preservados abaixo e nas pastas de origem. A licença dos textos jurídicos não concede licença sobre o software ou as marcas Symbios.

---

# Legal Templates

Attorney-drafted legal templates for startups and technology companies. Created by the attorneys at [General Legal](https://general.legal) and released under [CC0 1.0](LICENSE). Free for anyone to use, modify, and distribute for any purpose, without attribution.

These templates are provided in LLM-optimized markdown and original .docx formats. Highlighted text (marked with `<mark>` tags in the markdown files) indicates fields that should be customized for your use.

## Attribution

These templates include a General Legal credit footnote. The templates are released under CC0 1.0 Universal, so retaining that footnote isn't a legal requirement, but we ask that you keep it in place when reproducing or adapting these documents.

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

