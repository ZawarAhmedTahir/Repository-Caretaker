# Repository-Caretaker
Repository care taker is an AI agent that can:
1. Explore the repo(git status, list files, run linter).
2. Fix only small, safe things like: lint errors, formatting, unused imports, outdated requirements, explanatory comments, add TODO functions.
3. Never delete file, or make bug changes.
4. After fixes, run tests if any.
5. Never use git init to create new git project if project is non exist, just make changes directly in file.
6. If there is any TODO comment in the file then implement that function according to TODO description and write test cases for the function.
7. Finally commit with a clear conventional commit message.
8. Review files every for TODO comments or any other operation that can be performed according to instructions.

## Tech
1. This project uses pre trained model running locally to keep user repo data local.

## Upcoming changes
1. Project will have multiple agents having there own responsibilities and set of tools. 
2. Add handoffs