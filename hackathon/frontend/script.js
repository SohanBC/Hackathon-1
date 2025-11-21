/* ==========================================================
   BACKGROUND ANIMATION
========================================================== */
const canvas = document.getElementById("bgCanvas");
const ctx = canvas.getContext("2d");

function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resize();
window.onresize = resize;

let t = 0;
function animateBg() {
  t += 0.008;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let i = 0; i < 3; i++) {
    ctx.fillStyle = `rgba(75,114,255,${0.12 - i * 0.03})`;

    ctx.beginPath();
    ctx.moveTo(0, canvas.height / 2);

    for (let x = 0; x <= canvas.width; x += 6) {
      let y = Math.sin((x * 0.01) + t + i) * 40 + canvas.height / 2;
      ctx.lineTo(x, y);
    }

    ctx.lineTo(canvas.width, canvas.height);
    ctx.lineTo(0, canvas.height);
    ctx.fill();
  }

  requestAnimationFrame(animateBg);
}
animateBg();


/* ==========================================================
   LOTTIE ANIMATIONS
========================================================== */
lottie.loadAnimation({
  container: document.getElementById("lottie-hero"),
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "https://assets8.lottiefiles.com/packages/lf20_jcikwtux.json"
});

lottie.loadAnimation({
  container: document.getElementById("lottie-upload"),
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "https://assets8.lottiefiles.com/packages/lf20_x62chJ.json"
});

lottie.loadAnimation({
  container: document.getElementById("lottie-modal"),
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "https://assets6.lottiefiles.com/packages/lf20_touohxv0.json"
});


/* ==========================================================
   MODAL CONTROL
========================================================== */
function openModal(title, text) {
  document.getElementById("modalTitle").innerText = title;
  document.getElementById("modalText").innerText = text;

  const modal = document.getElementById("modal");
  modal.classList.remove("hide");
}

function closeModal() {
  const modal = document.getElementById("modal");
  modal.classList.add("hide");
}


/* ==========================================================
   URL SCAN (DEMO)
========================================================== */
function startURLScan() {
  const url = document.getElementById("urlInput").value.trim();
  const box = document.getElementById("urlResult");

  if (!url) return alert("Enter a valid URL!");

  openModal("Scanning URL", "Analyzing metadata...");

  setTimeout(() => {
    closeModal();

    const risk = Math.floor(20 + Math.random() * 70);

    box.classList.remove("hide");
    box.innerHTML = `
      <b>URL:</b> <a href="${url}" target="_blank">${url}</a><br><br>
      <b>Risk Score:</b> ${risk}%<br><br>
      <button class="btn" onclick="saveScan('${url}', ${risk})">Save to Dashboard</button>
    `;
  }, 2000);
}


/* ==========================================================
   APK SCAN (DEMO)
========================================================== */
const drop = document.getElementById("dropZone");
const apkInput = document.getElementById("apkInput");

drop.onclick = () => apkInput.click();

drop.ondragover = (e) => {
  e.preventDefault();
  drop.style.background = "rgba(75,114,255,0.2)";
};
drop.ondragleave = () => {
  drop.style.background = "transparent";
};

drop.ondrop = (e) => {
  e.preventDefault();
  let file = e.dataTransfer.files[0];
  handleFile(file);
};

apkInput.onchange = () => {
  handleFile(apkInput.files[0]);
};

function triggerUpload() {
  apkInput.click();
}

function handleFile(file) {
  if (!file.name.endsWith(".apk")) return alert("Only .apk files allowed!");

  openModal("Uploading...", "Running static analysis...");

  setTimeout(() => {
    closeModal();

    const risk = Math.floor(30 + Math.random() * 60);
    const box = document.getElementById("apkResult");

    box.classList.remove("hide");
    box.innerHTML = `
      <b>File:</b> ${file.name}<br><br>
      <b>Risk:</b> ${risk}%<br><br>
      <button class="btn" onclick="saveScan('${file.name}', ${risk})">Save to Dashboard</button>
    `;
  }, 2000);
}


/* ==========================================================
   DASHBOARD + CHART
========================================================== */
let scans = [];

function saveScan(name, risk) {
  const id = "scan-" + Date.now();

  scans.unshift({
    id,
    name,
    url: "https://play.google.com/store/apps/details?id=" + id,
    risk
  });

  updateDashboard();
  alert("Saved to dashboard!");
}

function updateDashboard() {
  const list = document.getElementById("recentList");
  list.innerHTML = "";

  scans.forEach(s => {
    list.innerHTML += `
      <div class="item">
        <div>
          <a href="${s.url}" target="_blank">${s.name}</a><br>
          <small>${s.id}</small>
        </div>
        <b>${s.risk}%</b>
      </div>
    `;
  });

  updateChart();
}


/* CHART */
let chartRef = null;
function updateChart() {
  const ctx = document.getElementById("riskChart").getContext("2d");

  if (chartRef) chartRef.destroy();

  chartRef = new Chart(ctx, {
    type: "line",
    data: {
      labels: scans.map(s => s.id).slice(0, 7),
      datasets: [{
        label: "Risk Score",
        data: scans.map(s => s.risk).slice(0, 7),
        borderColor: "#4b72ff",
        backgroundColor: "rgba(75,114,255,0.2)"
      }]
    },
    options: {
      responsive: true,
      scales: { y: { min: 0, max: 100 } }
    }
  });
}


/* ==========================================================
   EVIDENCE KIT
========================================================== */
function downloadEvidence() {
  const id = document.getElementById("scanIdInput").value.trim();
  if (!id) return alert("Enter scan ID");

  const fakeEvidence = {
    scanId: id,
    generatedAt: new Date().toISOString(),
    status: "DEMO VERSION"
  };

  const blob = new Blob([JSON.stringify(fakeEvidence, null, 2)], {
    type: "application/json"
  });

  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `${id}-evidence.json`;
  a.click();
}
