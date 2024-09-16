document.addEventListener('DOMContentLoaded', function() {
  let allowlistTextarea = document.getElementById('allowlist');
  let saveButton = document.getElementById('save');

  // Load the current allowlist
  chrome.storage.sync.get(['allowlist'], function(result) {
    if (result.allowlist) {
      allowlistTextarea.value = result.allowlist.join('\n');
    }
  });

  // Save the allowlist when the save button is clicked
  saveButton.addEventListener('click', function() {
    let allowlist = allowlistTextarea.value.split('\n').map(site => site.trim()).filter(site => site !== '');

    chrome.runtime.sendMessage({ action: "updateAllowlist", allowlist: allowlist });

    alert('Allowlist saved!');
  });
});
