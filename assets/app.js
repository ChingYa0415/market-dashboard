const fallbackData = {
  updatedAt: "2026-03-18T14:30:00+08:00",
  indices: [
    { label: "TAIEX", value: "22,418.76", changePct: 0.84, note: "AI 與電子權值續強" },
    { label: "NASDAQ", value: "18,206.11", changePct: 1.13, note: "成長股偏多" },
    { label: "BTC", value: "83,450", changePct: -0.62, note: "高檔震盪" },
    { label: "USD/TWD", value: "31.62", changePct: 0.15, note: "台幣略弱" },
  ],
  watchlist: [
    {
      symbol: "NVDA",
      name: "NVIDIA",
      price: 932.15,
      changePct: 2.42,
      volume: "High",
      thesis: "留意 AI 伺服器鏈帶動的延續性。",
      prices: [884, 892, 901, 908, 915, 924, 932],
    },
    {
      symbol: "TSM",
      name: "Taiwan Semi",
      price: 149.62,
      changePct: 1.18,
      volume: "Normal",
      thesis: "法說前觀察外資回補力道。",
      prices: [141, 142, 143, 145, 146, 148, 149.6],
    },
    {
      symbol: "QQQ",
      name: "Nasdaq ETF",
      price: 447.33,
      changePct: 0.51,
      volume: "Normal",
      thesis: "偏多趨勢未破，但追價風險上升。",
      prices: [438, 439, 440, 442, 444, 446, 447.3],
    },
    {
      symbol: "BTC",
      name: "Bitcoin",
      price: 83450,
      changePct: -0.62,
      volume: "High",
      thesis: "守住 82k 才有機會再攻。",
      prices: [86100, 85500, 85100, 84500, 84200, 83800, 83450],
    },
    {
      symbol: "AAPL",
      name: "Apple",
      price: 212.41,
      changePct: -1.04,
      volume: "Low",
      thesis: "短線轉弱，等待新催化。",
      prices: [219, 218, 217, 216, 215, 214, 212.4],
    },
  ],
  alerts: [
    { level: "high", title: "開盤前先確認重大財報", detail: "今晚留意美股盤後財報，決定隔日科技股風險暴露。" },
    { level: "medium", title: "台積電 ADR 與現股價差", detail: "若價差擴大，可作為隔日台股半導體情緒判斷。" },
    { level: "low", title: "記錄每筆進場理由", detail: "把觸發條件寫下來，方便日後回測與優化策略。" },
  ],
  playbook: [
    "先看大盤結構，再看個股，不要因為單一新聞就重押。",
    "單筆風險維持在總資金 0.5% 到 1%。",
    "若指數與領漲股背離，先縮手，不要硬追。",
    "重大事件前保留現金，提高彈性。",
  ],
};

const fallbackPremarketReport = {
  generatedAt: "2026-03-19T21:00:00+08:00",
  overview: {
    marketSentiment: "中性偏多",
    mainTheme: "AI 主線延續，但高位震盪加大",
    riskEvent: "留意盤後財報與 Fed 官員發言",
    focus: ["NVDA", "AMD", "ETN"],
  },
  core: [
    {
      symbol: "NVDA",
      news: "AI 伺服器需求仍為市場主線。",
      judgement: "趨勢未破，但不適合高位追價。",
      premarket: "+1.8%",
      openingBias: "利多",
      observation: "看開盤後是否站穩前高區。",
    },
    {
      symbol: "AMD",
      news: "市場關注 AI GPU 與資料中心節奏。",
      judgement: "屬於跟隨主線的高 Beta 標的。",
      premarket: "+0.9%",
      openingBias: "中性",
      observation: "若量能不足，容易轉震盪。",
    },
  ],
  watch: [
    {
      symbol: "ETN",
      news: "基建與電力題材持續被關注。",
      judgement: "若資金回流工業，容易成為輪動焦點。",
      premarket: "+0.6%",
      openingBias: "中性",
      observation: "留意能否守住五日線。",
    },
    {
      symbol: "GSAT",
      news: "今晚沒新聞",
      judgement: "小型題材股，波動大、延續性較差。",
      premarket: "資料不足",
      openingBias: "中性",
      observation: "只適合當情緒溫度計，不適合重押。",
    },
    {
      symbol: "ZETA",
      news: "市場偏向題材交易。",
      judgement: "高波動，高風險。",
      premarket: "+3.2%",
      openingBias: "利多",
      observation: "若開高走低，要特別防追高。",
    },
    {
      symbol: "RTX",
      news: "防禦型與工業股輪動觀察中。",
      judgement: "相對穩定，可當市場風格對照組。",
      premarket: "+0.2%",
      openingBias: "中性",
      observation: "看是否有資金回防大型防禦股。",
    },
  ],
  actionSummary: {
    mostImportant: ["NVDA", "AMD", "ETN"],
    coreView: "核心持股維持偏多思路，但不追高，等回踩或確認量價再動作。",
    highestVolatility: ["GSAT", "ZETA"],
    ifMarketWeakens: ["GSAT"],
  },
};

const state = {
  range: "1W",
  filter: "",
  currentSlide: 0,
  autoplay: true,
  autoplayTimer: null,
  data: fallbackData,
  premarketReport: fallbackPremarketReport,
};

const els = {
  lastUpdated: document.querySelector("#last-updated"),
  snapshotGrid: document.querySelector("#snapshot-grid"),
  watchlistBody: document.querySelector("#watchlist-body"),
  moversList: document.querySelector("#movers-list"),
  alertsList: document.querySelector("#alerts-list"),
  playbookList: document.querySelector("#playbook-list"),
  notes: document.querySelector("#desk-notes"),
  filter: document.querySelector("#symbol-filter"),
  slidesTrack: document.querySelector("#slides-track"),
  slidesDots: document.querySelector("#slides-dots"),
  slideCounter: document.querySelector("#slide-counter"),
  autoplayToggle: document.querySelector("#autoplay-toggle"),
  navButtons: [...document.querySelectorAll("[data-slide-nav]")],
};

init();

async function init() {
  const [dashboardData, premarketReport] = await Promise.all([loadDashboardData(), loadPremarketReport()]);
  state.data = dashboardData;
  state.premarketReport = premarketReport;
  hydrateNotes();
  bindEvents();
  render();
  syncSlide();
  restartAutoplay();
}

async function loadDashboardData() {
  try {
    const response = await fetch("./data/watchlist.json");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch {
    return fallbackData;
  }
}

async function loadPremarketReport() {
  try {
    const response = await fetch("./data/latest_premarket_report.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch {
    return fallbackPremarketReport;
  }
}

function bindEvents() {
  els.filter?.addEventListener("input", (event) => {
    state.filter = event.target.value.trim().toLowerCase();
    renderWatchlist();
    renderMovers();
  });

  els.notes?.addEventListener("input", (event) => {
    localStorage.setItem("market-dashboard:notes", event.target.value);
  });

  els.navButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const direction = button.dataset.slideNav;
      if (direction === "prev") {
        goToSlide(state.currentSlide - 1);
      } else {
        goToSlide(state.currentSlide + 1);
      }
      restartAutoplay();
    });
  });

  els.autoplayToggle?.addEventListener("click", () => {
    state.autoplay = !state.autoplay;
    renderAutoplayLabel();
    restartAutoplay();
  });
}

function hydrateNotes() {
  const saved = localStorage.getItem("market-dashboard:notes");
  if (saved && els.notes) {
    els.notes.value = saved;
  }
}

function render() {
  renderLastUpdated();
  renderSlides();
  renderSnapshots();
  renderWatchlist();
  renderMovers();
  renderAlerts();
  renderPlaybook();
  renderAutoplayLabel();
}

function renderLastUpdated() {
  if (!els.lastUpdated) {
    return;
  }
  const sourceTime = state.premarketReport.generatedAt ?? state.data.updatedAt;
  const text = new Date(sourceTime).toLocaleString("zh-TW", { hour12: false });
  els.lastUpdated.textContent = `最後更新 ${text}`;
}

function renderSlides() {
  if (!els.slidesTrack || !els.slidesDots) {
    return;
  }

  const slides = buildSlides(state.premarketReport);
  els.slidesTrack.innerHTML = slides.map(renderSlideCard).join("");
  els.slidesDots.innerHTML = slides
    .map(
      (_, index) => `
        <button
          type="button"
          class="slide-dot${index === state.currentSlide ? " is-active" : ""}"
          data-slide-index="${index}"
          aria-label="切換到第 ${index + 1} 張"
        ></button>
      `,
    )
    .join("");

  [...els.slidesDots.querySelectorAll("[data-slide-index]")].forEach((button) => {
    button.addEventListener("click", () => {
      goToSlide(Number(button.dataset.slideIndex || 0));
      restartAutoplay();
    });
  });

  syncSlide();
}

function buildSlides(report) {
  const coreBlocks = report.core ?? [];
  const watchBlocks = report.watch ?? [];

  return [
    {
      kicker: "Slide 01",
      title: "今晚總覽",
      body: `
        <div class="story-grid cols-2">
          <div class="story-metric">
            <span>市場情緒</span>
            <strong>${report.overview.marketSentiment}</strong>
          </div>
          <div class="story-metric">
            <span>主線題材</span>
            <strong>${report.overview.mainTheme}</strong>
          </div>
          <div class="story-metric">
            <span>風險事件</span>
            <strong>${report.overview.riskEvent}</strong>
          </div>
          <div class="story-metric">
            <span>優先關注</span>
            <strong>${(report.overview.focus ?? []).join("、")}</strong>
          </div>
        </div>
      `,
    },
    {
      kicker: "Slide 02",
      title: "核心持股",
      body: `
        <div class="story-list">
          ${coreBlocks.map(renderReportItem).join("")}
        </div>
      `,
    },
    {
      kicker: "Slide 03",
      title: "觀察股",
      body: `
        <div class="story-list compact-list">
          ${watchBlocks.map(renderReportItem).join("")}
        </div>
      `,
    },
    {
      kicker: "Slide 04",
      title: "行動摘要",
      body: `
        <div class="story-grid">
          <div class="story-metric wide">
            <span>最值得注意</span>
            <strong>${(report.actionSummary.mostImportant ?? []).join("、")}</strong>
          </div>
          <div class="story-metric wide">
            <span>核心持股看法</span>
            <strong>${report.actionSummary.coreView}</strong>
          </div>
          <div class="story-metric">
            <span>高波動名單</span>
            <strong>${(report.actionSummary.highestVolatility ?? []).join("、")}</strong>
          </div>
          <div class="story-metric">
            <span>市場轉弱先留意</span>
            <strong>${(report.actionSummary.ifMarketWeakens ?? []).join("、")}</strong>
          </div>
        </div>
      `,
    },
  ];
}

function renderSlideCard(slide) {
  return `
    <article class="story-slide">
      <p class="section-kicker">${slide.kicker}</p>
      <h3>${slide.title}</h3>
      ${slide.body}
    </article>
  `;
}

function renderReportItem(item) {
  return `
    <article class="story-item">
      <div class="story-item-head">
        <strong>${item.symbol}</strong>
        <span class="bias-pill ${getBiasClass(item.openingBias)}">${item.openingBias}</span>
      </div>
      <p><span>新聞</span>${item.news}</p>
      <p><span>判讀</span>${item.judgement}</p>
      <p><span>盤前</span>${item.premarket}</p>
      <p><span>觀察</span>${item.observation}</p>
    </article>
  `;
}

function syncSlide() {
  if (!els.slidesTrack || !els.slideCounter || !els.slidesDots) {
    return;
  }
  const slideCount = els.slidesTrack.children.length || 1;
  state.currentSlide = ((state.currentSlide % slideCount) + slideCount) % slideCount;
  els.slidesTrack.style.transform = `translateX(-${state.currentSlide * 100}%)`;
  els.slideCounter.textContent = `${state.currentSlide + 1} / ${slideCount}`;
  [...els.slidesDots.children].forEach((dot, index) => {
    dot.classList.toggle("is-active", index === state.currentSlide);
  });
}

function goToSlide(index) {
  state.currentSlide = index;
  syncSlide();
}

function restartAutoplay() {
  window.clearInterval(state.autoplayTimer);
  if (!state.autoplay) {
    return;
  }
  state.autoplayTimer = window.setInterval(() => {
    goToSlide(state.currentSlide + 1);
  }, 5000);
}

function renderAutoplayLabel() {
  if (els.autoplayToggle) {
    els.autoplayToggle.textContent = `自動播放：${state.autoplay ? "開" : "關"}`;
  }
}

function renderSnapshots() {
  if (!els.snapshotGrid) {
    return;
  }
  els.snapshotGrid.innerHTML = state.data.indices
    .map(
      (item) => `
        <article class="snapshot-card">
          <div class="label">${item.label}</div>
          <div class="value">${item.value}</div>
          <div class="sub ${item.changePct >= 0 ? "positive" : "negative"}">
            ${formatSigned(item.changePct)}%
          </div>
          <div class="sub">${item.note}</div>
        </article>
      `,
    )
    .join("");
}

function renderWatchlist() {
  if (!els.watchlistBody) {
    return;
  }
  const rows = getFilteredWatchlist()
    .map(
      (item) => `
        <tr>
          <td>
            <div class="symbol-cell">
              <strong>${item.symbol}</strong>
              <span>${item.name}</span>
            </div>
          </td>
          <td>${formatPrice(item.price)}</td>
          <td class="${item.changePct >= 0 ? "positive" : "negative"}">${formatSigned(item.changePct)}%</td>
          <td>${item.volume}</td>
          <td>${renderSparkline(item.prices, item.changePct >= 0)}</td>
          <td>${item.thesis}</td>
        </tr>
      `,
    )
    .join("");
  els.watchlistBody.innerHTML = rows || `<tr><td colspan="6">沒有符合條件的標的。</td></tr>`;
}

function renderMovers() {
  if (!els.moversList) {
    return;
  }
  const movers = [...getFilteredWatchlist()]
    .sort((a, b) => Math.abs(b.changePct) - Math.abs(a.changePct))
    .slice(0, 4);

  els.moversList.innerHTML = movers
    .map(
      (item) => `
        <article class="mover-item">
          <div class="mover-meta">
            <strong>${item.symbol}</strong>
            <span>${item.name}</span>
          </div>
          <strong class="${item.changePct >= 0 ? "positive" : "negative"}">
            ${formatSigned(item.changePct)}%
          </strong>
        </article>
      `,
    )
    .join("");
}

function renderAlerts() {
  if (!els.alertsList) {
    return;
  }
  els.alertsList.innerHTML = state.data.alerts
    .map(
      (alert) => `
        <article class="alert-item">
          <span class="alert-level ${alert.level}">${alert.level}</span>
          <strong>${alert.title}</strong>
          <p>${alert.detail}</p>
        </article>
      `,
    )
    .join("");
}

function renderPlaybook() {
  if (!els.playbookList) {
    return;
  }
  els.playbookList.innerHTML = state.data.playbook.map((item) => `<li>${item}</li>`).join("");
}

function getFilteredWatchlist() {
  if (!state.filter) {
    return state.data.watchlist;
  }
  return state.data.watchlist.filter((item) => {
    const haystack = `${item.symbol} ${item.name}`.toLowerCase();
    return haystack.includes(state.filter);
  });
}

function getBiasClass(value = "") {
  if (value.includes("利多")) return "bullish";
  if (value.includes("利空")) return "bearish";
  return "neutral";
}

function formatSigned(value) {
  return value >= 0 ? `+${value.toFixed(2)}` : value.toFixed(2);
}

function formatPrice(value) {
  if (value >= 1000) {
    return Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(value);
  }
  return value.toFixed(2);
}

function renderSparkline(points, positive) {
  const width = 120;
  const height = 44;
  const min = Math.min(...points);
  const max = Math.max(...points);
  const spread = max - min || 1;
  const coords = points
    .map((point, index) => {
      const x = (index / (points.length - 1)) * width;
      const y = height - ((point - min) / spread) * (height - 6) - 3;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
  const stroke = positive ? "#35c2a1" : "#ff6b7d";
  return `
    <svg class="sparkline" viewBox="0 0 ${width} ${height}" aria-hidden="true">
      <polyline points="${coords}" style="stroke:${stroke}"></polyline>
    </svg>
  `;
}
