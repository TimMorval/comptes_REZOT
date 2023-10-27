@echo off

:: Installer les modules Node.js si nécessaire
if not exist "node_modules\" (
    echo Installation des modules Node.js...
    npm install
)

:: Lancer npm start
echo Lancement de npm start...
npm start

:: Ouvrir le navigateur à l'adresse localhost:3000
start http://localhost:3000
