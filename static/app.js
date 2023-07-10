async function getGptResponse() {
  const firstPart = document.getElementById('firstPart').value;
  const animal = document.getElementById('animal').value;

  document.getElementById('chatLog').innerHTML += 'You: ' + firstPart + ' ' + animal + '<br>';

  const response = await fetch('/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: `firstPart=${firstPart}&animal=${animal}`
  });

  const redirectUrl = new URL(response.url);
  const result = redirectUrl.searchParams.get("result");

  document.getElementById('chatLog').innerHTML += 'GPT-4: ' + result + '<br>';
  document.getElementById('firstPart').value = '';
  document.getElementById('animal').value = '';
}
