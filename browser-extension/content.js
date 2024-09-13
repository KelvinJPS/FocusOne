chrome.runtime.sendMessage({ action: "checkIfBlocked" }, function(response) {
  if (response.blocked) {
    document.documentElement.innerHTML = '';
    fetch(chrome.runtime.getURL('blocked.html'))
      .then(response => response.text())
      .then(data => {
        document.write(data);
        document.close();
      });
  }
});

