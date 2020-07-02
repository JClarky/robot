@echo off
set /p commitName="Commit name: "
git add .
git commit -m "%commitName%"
git push