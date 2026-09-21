# Class 28 · Permissions as code

September 23, 2026 · 12 slides in English · 30-minute core, expandable to 60.

Continue the established lesson27 visual and image-generation workflow. HTML/PNG and Spanish HTML/Markdown guide. No speech or PPTX.

## 01. Permissions as code
- Class 28 · Week 6 · September 23, 2026
- Juan Maldonado
- Users, groups, ACLs and Repo Init
- Visual (cover): Large title left. Right: repository tree, identity and small key motif. Plenty of whitespace.

## 02. Access starts with an identity
- A human user performs an interactive action.
- A group represents a shared responsibility.
- A service user gives application code a repository identity.
- Each operation needs permission on its target path.
- Visual (concept): Three labeled identity symbols Human user, Group, Service user connect to one repository path and an operation check. Do not imply a group logs in.

## 03. Cloud identity and content access
- IMS authenticates people on Cloud Author.
- Admin Console product profiles grant environment access.
- AEM groups and ACLs define content operations.
- Repository service users have no password login.
- Visual (comparison): Two lanes: Human access shows IMS, environment access, AEM permissions. Application lane shows repository service user and scoped ACL. No token or mapping code. Small footer: Local demo users do not reproduce IMS provisioning.

## 04. An ACL describes access rules
- Principal: who the entry applies to.
- Path: where the entry takes effect.
- Privilege: which operation it covers.
- Allow or deny, with optional restrictions.
- Visual (definition): Annotate a single legible ACE: training-guide-editors /content/training-permissions/guides jcr:modifyProperties allow. Define ACL = list of entries; ACE = one entry. Do not add code.

## 05. Least privilege for one task
- Read content: jcr:read
- Change properties: jcr:modifyProperties
- Add child nodes: jcr:addChildNodes
- jcr:write bundles several write privileges.
- Visual (scope): Repository tree root /content/training-permissions with sibling guides and outside. Group read on root. Green property-edit marker only at guides. No edit marker on outside. Footer: This demo does not grant page creation, deletion or publication.

## 06. Effective access includes inherited rules
- Inspect the user and every relevant group.
- Follow ACLs from the target through its ancestors.
- Check entry order and restrictions.
- A narrow grant does not revoke broader access.
- Visual (diagnosis): Layered diagram: Target ACL, Ancestor ACLs, User and group principals feed Effective access. Orange caution: Deny does not always win. Footer: Verify the actual identity, path and operation.

## 07. Repo Init in source control
- Create the required paths and identities first.
- Assign ACLs to the smallest useful subtree.
- Store the script in an OSGi factory configuration.
- Use config.author for this Author-only example.
- Visual (process): Four-step vertical or horizontal process from Script to OSGi configuration to Repository initialization to Paths + identities + ACLs. Footer: Cloud delivery uses the project pipeline. Today uses local SDK.

## 08. A small permission model
- Group: training-guide-editors
- Service user: training-guide-reader
- Human group: read root, modify properties in guides.
- Service user: read guides.
- Visual (code): Show this exact short complete code block in large monospace on right: set ACL for training-guide-editors
  allow jcr:read on /content/training-permissions
  allow jcr:modifyProperties on /content/training-permissions/guides
end
Left contains four key points. Footer: ACL excerpt. Full configuration and setup are in the study guide. No wrapping within privilege names.

## 09. Local configuration and inspection
- Install the supplied Author configuration.
- Inspect the created group, service user and paths.
- Create a local demo user and add the editor group.
- Inspect inherited ACLs before checking the matrix.
- Visual (demo): Four ordered steps with precise folder, group, user and audit symbols. Footer: Local SDK only. No Cloud Manager access required. Include small note: The demo uses folders, not authorable pages.

## 10. Allowed and excluded operations
- Demo user belongs only to the editor group.
- Read guides: expected allowed.
- Modify guides properties: expected allowed.
- Modify outside properties: expected denied.
- Visual (matrix): Large 3-row table Operation / Target / Expected: Read / guides / Allowed; Modify properties / guides / Allowed; Modify properties / outside / Denied. Render key points only once by folding them into table and a setup sentence. Footer: Expected on a clean fixture. Inherited grants can change the result. Label table Expected checks, not measured results.

## 11. Key takeaways
- Separate human authentication from repository authorization.
- Give service users a specific technical responsibility.
- Scope privileges to the paths the task requires.
- Inspect effective access, including inherited grants.
- Version Repo Init and check allowed and excluded operations.
- Visual (summary): Five wide takeaway rows with discreet specific icons. No duplicate bullets. Spacious, readable type.

## 12. Questions / Thank you.
- Questions
- Thank you.
- Visual (closing): Passive closing. Render ONLY Questions, Thank you. and the number 12. Abstract speech bubble and quiet repository motif; no footer, metadata, additional prompt or exercise.
