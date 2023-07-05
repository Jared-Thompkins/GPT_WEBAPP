async function getGptResponse() {
  const userInput = document.getElementById('userInput').value;
  document.getElementById('chatLog').innerHTML += 'You: ' + userInput + '<br>';
  
  const response = await fetch('http://localhost:5000/get-response', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: userInput
    })
  });
  
  const data = await response.json();

  document.getElementById('chatLog').innerHTML += 'GPT-4: ' + data.response + '<br>';
  document.getElementById('userInput').value = '';
}