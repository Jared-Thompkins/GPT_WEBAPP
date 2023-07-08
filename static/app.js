async function getGptResponse() {
  const userInput = document.getElementById('userInput').value;
  document.getElementById('chatLog').innerHTML += 'You: ' + userInput + '<br>';

  const response = await fetch('/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `animal=${userInput}`
  });

  const redirectUrl = new URL(response.url);
  const result = redirectUrl.searchParams.get("result");

  document.getElementById('chatLog').innerHTML += 'GPT-4: ' + result + '<br>';
  document.getElementById('userInput').value = '';
}
