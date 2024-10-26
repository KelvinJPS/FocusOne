/*
 */
let port = browser.runtime.connectNative("focusone");

/*
Listen for messages from the app.
*/
port.onMessage.addListener((response) => {
  console.log(`Received: ${response}`);
});

/*
On a click on the browser action, send the app a message.
*/
browser.browserAction.onClicked.addListener(() => {
  console.log("Sending:  ping");
  port.postMessage("ping");
});

// /*blocking functionality/
// let allowedWebsites = [];
//
// chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
//   if (message.type === "setAllowedWebsites") {
//     allowedWebsites = message.websites;
//     updateBlockingRules();
//   }
// });
//
// chrome.runtime.onInstalled.addListener(() => {
//   chrome.declarativeNetRequest.updateDynamicRules({
//     removeRuleIds: [1],
//     addRules: [
//       {
//         id: 1,
//         priority: 1,
//         action: { type: "block" },
//         condition: { urlFilter: "*://*/*", resourceTypes: ["main_frame"] },
//       },
//     ],
//   });
// });
//
// function updateBlockingRules() {
//   const rules = [
//     {
//       id: 1,
//       priority: 1,
//       action: { type: "block" },
//       condition: {
//         urlFilter: "*://*/*",
//         resourceTypes: ["main_frame"],
//         excludedRequestDomains: allowedWebsites,
//       },
//     },
//   ];
//
//   chrome.declarativeNetRequest.updateDynamicRules({
//     removeRuleIds: [1],
//     addRules: rules,
//   });
// }
//
// chrome.runtime.onMessageExternal.addListener(
//   (message, sender, sendResponse) => {
//     if (message.allowed_websites) {
//       allowedWebsites = message.allowed_websites;
//       updateBlockingRules();
//       sendResponse({ success: true });
//     }
//   },
// );
