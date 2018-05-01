Archivematica FPR tools
=======================

NOTE: As of the 1.7 version of Archivematica, the FPR server has been decoupled from Archivematica. Please see the [release notes](https://wiki.archivematica.org/Archivematica_1.7_and_Storage_Service_0.11_release_notes#Archivematica_decoupled_from_the_FPR_server). Issue creation has been disabled for this
repository.

This repository contains the source code to the scripts maintained in the [Archivematica FPR](https://github.com/artefactual/archivematica-fpr-admin) database.
Because the tools are maintained in a database in FPR server and Archivematica installations, diffing the version history and running `git blame` is inconvenient; this repository is meant to make such tasks simpler.

Deployment process
------------------

When creating a new tool or updating an existing tool, follow these steps to deploy:

1. Add a new script to the appropriate path, or update the existing script.
2. Create a pull request.
3. When code review is complete, use the [add-fpr-rule](https://github.com/artefactual/archivematica-devtools/blob/master/tools/add-fpr-rule) tool from the Archivematica devtools to add the new tool or update an existing one. This will generate SQL.
4. Use that SQL to deploy to the FPR server.
5. Add the SQL as a migration to Archivematica.
6. Merge the branch.
