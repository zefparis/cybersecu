const fs = require('fs');
const { exec } = require('child_process');

console.log('Building CSS with Tailwind...');

exec('npx tailwindcss -i ./static/src/input.css -o ./static/css/styles.css', (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`stderr: ${stderr}`);
    return;
  }
  console.log('CSS build successful!');
  console.log(stdout);
});
