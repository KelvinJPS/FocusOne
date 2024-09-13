let allowlist = [];

chrome.storage.sync.get(['allowlist'], function(result) {
  if (result.allowlist) {
    allowlist = result.allowlist;
    updateRules();
  }
});

function updateRules() {
  chrome.declarativeNetRequest.updateDynamicRules({
    removeRuleIds: [1],
    addRules: [{
      id: 1,
      priority: 1,
      action: { type: 'allow' },
      condition: {
        urlFilter: '*',
        domains: allowlist
      },
    }]
  });
}

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.action === "updateAllowlist") {
      allowlist = request.allowlist;
      chrome.storage.sync.set({ allowlist: allowlist });
      updateRules();
    } else if (request.action === "checkIfBlocked") {
      let url = new URL(sender.tab.url);
      let domain = url.hostname;
      sendResponse({ blocked: !allowlist.some(site => domain.includes(site)) });
    }
  }
);
