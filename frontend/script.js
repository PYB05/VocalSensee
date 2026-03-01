// Navigation functionality
const navLinks = document.getElementById('navLinks');
const hamburger = document.getElementById('hamburger');
const pages = document.querySelectorAll('.page');
const navItems = document.querySelectorAll('.nav-link');

hamburger.addEventListener('click', () => {
  navLinks.classList.toggle('active');
});

navItems.forEach(item => {
  item.addEventListener('click', (e) => {
    e.preventDefault();
    const pageId = item.getAttribute('data-page');

    pages.forEach(page => page.classList.remove('active'));
    document.getElementById(`${pageId}-page`).classList.add('active');

    navItems.forEach(navItem => navItem.classList.remove('active'));
    item.classList.add('active');

    navLinks.classList.remove('active');
  });
});

// Demo page functionality
const fileInput = document.getElementById('audioFile');
const predictButton = document.getElementById('predictButton');
const filenameDisplay = document.getElementById('filename');

fileInput.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    predictButton.disabled = false;
    filenameDisplay.textContent = `Selected: ${e.target.files[0].name}`;
  } else {
    predictButton.disabled = true;
    filenameDisplay.textContent = '';
  }
});

predictButton.addEventListener('click', uploadAndPredict);

async function uploadAndPredict() {
  const file = fileInput.files[0];
  if (!file) return;

  predictButton.disabled = true;
  predictButton.textContent = 'Analyzing...';

  const resultContainer = document.querySelector('.result-container');
  resultContainer.innerHTML = `
    <div class="loading-wave">
      <div class="loading-bar"></div>
      <div class="loading-bar"></div>
      <div class="loading-bar"></div>
      <div class="loading-bar"></div>
    </div>
    <p style="text-align: center; margin-top: 1rem;">Analyzing voice patterns...</p>
  `;

  const formData = new FormData();
  formData.append("file", file);

  const startTime = Date.now();
  const minimumDelay = 2000;

  try {
    const response = await fetch("https://vocalsense-backend.onrender.com/predict", {
      method: "POST",
      body: formData,
      headers: {
        "Accept": "application/json"
      }
    });

    const elapsedTime = Date.now() - startTime;
    const remainingDelay = Math.max(0, minimumDelay - elapsedTime);
    if (remainingDelay > 0) await new Promise(resolve => setTimeout(resolve, remainingDelay));

    if (!response.ok) {
      throw new Error(`Server responded with status ${response.status}`);
    }

    const result = await response.json();
    if (result.prediction) {
      resultContainer.innerHTML = `
        <h2 id="result" class="result-animation">
          Detected emotion: <strong>${result.prediction}</strong>
        </h2>
      `;
    } else {
      resultContainer.innerHTML = `
        <h2 id="result" class="result-animation">
          Error: ${result.error || "Unknown error occurred"}
        </h2>
      `;
    }

  } catch (error) {
    console.error("Prediction error:", error);
    resultContainer.innerHTML = `
      <h2 id="result" class="result-animation">
        Network error: ${error.message}
      </h2>
    `;
  } finally {
    predictButton.disabled = false;
    predictButton.textContent = 'Analyze Emotion';
  }
}

// Dark mode toggle
const darkModeToggle = document.getElementById('darkModeToggle');
const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

if (localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && prefersDarkScheme.matches)) {
  document.documentElement.setAttribute('data-theme', 'dark');
  darkModeToggle.checked = true;
}

darkModeToggle.addEventListener('change', () => {
  if (darkModeToggle.checked) {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('theme', 'light');
  }
});

// Settings page functionality
const audioQualitySelect = document.getElementById('audioQuality');
const languageSelect = document.getElementById('languageSelect');

if (localStorage.getItem('audioQuality')) {
  audioQualitySelect.value = localStorage.getItem('audioQuality');
}
if (localStorage.getItem('language')) {
  languageSelect.value = localStorage.getItem('language');
}

audioQualitySelect.addEventListener('change', () => {
  localStorage.setItem('audioQuality', audioQualitySelect.value);
});

languageSelect.addEventListener('change', () => {
  localStorage.setItem('language', languageSelect.value);
});
