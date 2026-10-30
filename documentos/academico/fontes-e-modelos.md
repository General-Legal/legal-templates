# Modelos abertos e referências jurídicas

**Consulta:** 29/10/2026. Comparação para a versão acadêmica da Symbios; as avaliações de adequação são conclusões desta análise, não certificações dos projetos.

## Quatro opções

| Opção e fonte | Licença verificada | Avaliação para a Symbios |
| --- | --- | --- |
| [General Legal](https://github.com/General-Legal/legal-templates) | [CC0 1.0](https://github.com/General-Legal/legal-templates/blob/main/LICENSE) | Recomendado: reúne Termos, Política GDPR e DPA; permite adaptação sem atribuição obrigatória. Exige substituir regras estrangeiras e tratar expressamente dados de saúde. |
| [Automattic / Legalmattic](https://github.com/Automattic/legalmattic) | [CC BY-SA 4.0, indicada no README](https://github.com/Automattic/legalmattic#license) | Alternativa para regras de serviço e transparência; exige atribuição e licenciamento das adaptações compartilhadas sob a mesma licença. A obrigação recai sobre o texto adaptado, não automaticamente sobre o software. |
| [Privacy Policy Templates — ryuno2525 / PolicyForge](https://github.com/ryuno2525/privacy-policy-templates) | [MIT](https://github.com/ryuno2525/privacy-policy-templates/blob/main/LICENSE) | Estrutura simples para sites, aplicativos e SaaS; preservar aviso de copyright e licença nas cópias ou partes substanciais. A menção à LGPD no projeto não comprova adequação a dados clínicos. |
| [App Privacy Policy Generator — nisrulz](https://github.com/nisrulz/app-privacy-policy-generator) | [AGPL-3.0 da ferramenta](https://github.com/nisrulz/app-privacy-policy-generator/blob/master/LICENSE) | Gerador de estrutura inicial; não selecionado como base. A licença do programa, isoladamente, não resolve a licença de todo texto gerado: conferir o conteúdo e os avisos aplicáveis antes de reaproveitar a saída. |

Documentos jurídicos com licenças abertas podem ser reutilizados, mas isso não atesta conformidade com a legislação brasileira. A licença aberta dos modelos também não torna o software Symbios open source.

## Fontes brasileiras

| Referência oficial | Aplicação nesta adaptação |
| --- | --- |
| [LGPD — Lei nº 13.709/2018, texto atualizado da Câmara](https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-normaatualizada-pl.html) | Arts. 4º, II, b; 5º; 6º–14; 15–20; 33–39; 42–49: regime acadêmico, agentes, bases legais, saúde, anonimização, direitos, transferências e segurança. |
| [Código de Defesa do Consumidor — Lei nº 8.078/1990, texto atualizado da Câmara](https://www2.camara.leg.br/legin/fed/lei/1990/lei-8078-11-setembro-1990-365086-normaatualizada-pl.html) | Garantias e responsabilidade nas relações de consumo, quando aplicáveis, e limites a cláusulas de exoneração, renúncia e arbitragem compulsória. |
| [Código Civil — Lei nº 10.406/2002, texto atualizado da Câmara](https://www2.camara.leg.br/legin/fed/lei/2002/lei-10406-10-janeiro-2002-432893-normaatualizada-pl.pdf) | Boa-fé, interpretação dos contratos de adesão e reparação de danos na adaptação das cláusulas de indenização e responsabilidade. |
| [Lei do Software — Lei nº 9.609/1998, texto atualizado da Câmara](https://www2.camara.leg.br/legin/fed/lei/1998/lei-9609-19-fevereiro-1998-364738-normaatualizada-pl.html) | Permissões legais de uso e reprodução, validade técnica e serviços técnicos obrigatórios, especialmente arts. 6º a 8º. |
| [Lei de Arbitragem — Lei nº 9.307/1996, texto atualizado da Câmara](https://www2.camara.leg.br/legin/fed/lei/1996/lei-9307-23-setembro-1996-349058-normaatualizada-pl.html) | Requisitos da convenção de arbitragem e concordância específica em contratos de adesão, especialmente art. 4º, § 2º. |
| [Lei nº 14.879/2024 — alteração do art. 63 do CPC](https://presidencia.gov.br/ccivil_03/_ato2023-2026/2024/lei/l14879.htm) | Pertinência da eleição de foro com o domicílio das partes ou local da obrigação e preservação das regras consumeristas aplicáveis. |
| [Guia da ANPD sobre fins acadêmicos e estudos e pesquisas](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-tratamento-de-dados-pessoais-para-fins-academicos-e-para-a-realizacao-de-estudos-e-pesquisas) | O regime de atividades exclusivamente acadêmicas exige análise concreta e preserva os arts. 7º e 11. Uma empresa ou projeto não se torna órgão de pesquisa apenas por atuar com universidades. |
| [Resolução CD/ANPD nº 15/2024 — texto oficial no Ministério da Justiça](https://bibliotecadigital.mj.gov.br/bitstream/1/12879/2/RES_ANPD_2024_15.html) | Incidentes: comunicação pelo controlador à ANPD e aos titulares, em regra em três dias úteis, quando houver risco ou dano relevante, observadas as hipóteses e regras aplicáveis. |
| [Resolução CD/ANPD nº 19/2024 — texto disponibilizado pela ANPD](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-19-de-23-de-agosto-de-2024) | Transferência internacional: base legal do tratamento e mecanismo válido; adoção integral e sem alteração das cláusulas-padrão brasileiras quando esse for o mecanismo escolhido. |

## Adaptações principais

- Termos: seguir a estrutura de onze seções do modelo original e preservar as proteções da Symbios, inclusive indenização, restrições de uso, licença de sugestões, isenções, exclusões e teto de responsabilidade; adaptar moeda, foro, arbitragem e normas obrigatórias ao contexto brasileiro. O valor mínimo do teto em reais permanece para definição comercial. Ver [revisão comparativa](revisao-termos-de-uso.md).
- Privacidade: retirar finalidades genéricas de publicidade e listas de coleta não confirmadas; identificar a empresa e criar inventário por finalidade e base legal.
- DPA: contemplar dados reais de saúde, instruções, fornecedores, segurança, incidentes, retenção e anonimização; não importar automaticamente anexos GDPR, HIPAA ou cláusulas europeias.
- Melhorias e treinamentos: permitir somente dados efetivamente anonimizados; exigir análise jurídica e técnica da etapa de anonimização e vedar reidentificação.

As referências normativas orientam a minuta. A publicação depende da confirmação dos fluxos reais, do preenchimento dos campos e de revisão jurídica.
