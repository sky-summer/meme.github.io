const PREVIEW_CONCURRENCY = 4;

const state = {
  memes: [],
  selected: null,
  imageFiles: [],
  textCount: 0,
};

const el = {
  search: document.getElementById("search"),
  previewSwitch: document.getElementById("previewSwitch"),
  memeList: document.getElementById("memeList"),
  count: document.getElementById("count"),
  randomBtn: document.getElementById("randomBtn"),
  version: document.getElementById("version"),
  placeholder: document.getElementById("placeholder"),
  detail: document.getElementById("detail"),
  dKey: document.getElementById("dKey"),
  dKeywords: document.getElementById("dKeywords"),
  dMeta: document.getElementById("dMeta"),
  dPreview: document.getElementById("dPreview"),
  imagesArea: document.getElementById("imagesArea"),
  imagesBox: document.getElementById("imagesBox"),
  imagesHint: document.getElementById("imagesHint"),
  textsArea: document.getElementById("textsArea"),
  textsBox: document.getElementById("textsBox"),
  textsHint: document.getElementById("textsHint"),
  generateBtn: document.getElementById("generateBtn"),
  status: document.getElementById("status"),
  resultBox: document.getElementById("resultBox"),
  resultImg: document.getElementById("resultImg"),
  downloadBtn: document.getElementById("downloadBtn"),
};

/* ---------------- 预览图懒加载 ---------------- */

const previewQueue = new Set();
const previewLoading = new Map();
// 已经确认生成失败的表情，不再重复请求，避免服务端反复报错
const previewFailed = new Set();
let previewActive = 0;

const observer = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) requestPreview(entry.target);
      else cancelPreview(entry.target);
    }
  },
  { root: el.memeList, rootMargin: "400px 0px" }
);

function requestPreview(item) {
  if (!el.previewSwitch.checked) return;
  if (previewFailed.has(item.dataset.key)) return;
  if (item.dataset.previewState || previewQueue.has(item)) return;
  previewQueue.add(item);
  pumpPreview();
}

function cancelPreview(item) {
  const controller = previewLoading.get(item);
  if (controller) {
    controller.abort();
    previewLoading.delete(item);
    previewActive--;
    delete item.dataset.previewState;
    pumpPreview();
  } else {
    previewQueue.delete(item);
  }
}

function pumpPreview() {
  while (previewActive < PREVIEW_CONCURRENCY && previewQueue.size > 0) {
    const item = previewQueue.values().next().value;
    previewQueue.delete(item);
    loadPreview(item);
  }
}

function loadPreview(item) {
  const key = item.dataset.key;
  const img = item.querySelector("img");
  if (!img) return;

  item.dataset.previewState = "loading";
  img.classList.add("loading");

  const controller = new AbortController();
  previewLoading.set(item, controller);
  previewActive++;

  fetch(`/memes/${encodeURIComponent(key)}/preview`, { signal: controller.signal })
    .then((res) => (res.ok ? res.blob() : Promise.reject(new Error(String(res.status)))))
    .then((blob) => {
      img.src = URL.createObjectURL(blob);
      item.dataset.previewState = "done";
    })
    .catch(() => {
      delete item.dataset.previewState;
      if (!controller.signal.aborted) {
        previewFailed.add(key);
        item.dataset.previewState = "failed";
      }
    })
    .finally(() => {
      img.classList.remove("loading");
      previewLoading.delete(item);
      previewActive--;
      pumpPreview();
    });
}

/* ---------------- 列表渲染 ---------------- */

function renderList() {
  const keyword = el.search.value.trim().toLowerCase();
  const memes = keyword
    ? state.memes.filter(
        (m) =>
          m.key.toLowerCase().includes(keyword) ||
          (m.keywords || []).some((k) => k.toLowerCase().includes(keyword))
      )
    : state.memes;

  el.count.textContent = `共 ${memes.length} 个表情`;

  for (const item of Array.from(el.memeList.children)) {
    observer.unobserve(item);
    cancelPreview(item);
  }
  el.memeList.innerHTML = "";

  const fragment = document.createDocumentFragment();
  for (const meme of memes) {
    const item = document.createElement("div");
    item.className = "meme-item";
    item.dataset.key = meme.key;
    if (state.selected && state.selected.key === meme.key) item.classList.add("active");

    const img = document.createElement("img");
    img.className = "meme-thumb";
    img.alt = meme.key;

    const info = document.createElement("div");
    info.className = "meme-info";
    const name = document.createElement("div");
    name.className = "meme-name";
    name.textContent = (meme.keywords && meme.keywords[0]) || meme.key;
    const key = document.createElement("div");
    key.className = "meme-key";
    key.textContent = meme.key;
    info.append(name, key);

    item.append(img, info);
    item.addEventListener("click", () => selectMeme(meme.key));
    fragment.append(item);
    observer.observe(item);
  }
  el.memeList.append(fragment);
}

function highlightActive() {
  for (const item of el.memeList.children) {
    item.classList.toggle(
      "active",
      !!state.selected && item.dataset.key === state.selected.key
    );
  }
}

/* ---------------- 表单构建 ---------------- */

function rangeText(min, max) {
  if (min === max) return `${min} 个`;
  return `${min} ~ ${max} 个`;
}

function buildImageSlots(meme) {
  el.imagesBox.innerHTML = "";
  state.imageFiles = [];
  const { min_images: minImages, max_images: maxImages } = meme;

  if (maxImages <= 0) {
    el.imagesArea.classList.add("hidden");
    return;
  }
  el.imagesArea.classList.remove("hidden");
  el.imagesHint.textContent = `需要 ${rangeText(minImages, maxImages)}`;

  for (let i = 0; i < minImages; i++) addImageSlot(i);
  if (minImages < maxImages) {
    const add = document.createElement("div");
    add.className = "dropzone empty";
    add.textContent = "+ 添加";
    add.addEventListener("click", () => {
      if (state.imageFiles.filter(Boolean).length >= maxImages) return;
      addImageSlot(state.imageFiles.length);
      add.remove();
      if (state.imageFiles.filter(Boolean).length < maxImages)
        el.imagesBox.append(add);
    });
    el.imagesBox.append(add);
  }
}

function addImageSlot(index) {
  const zone = document.createElement("div");
  zone.className = "dropzone empty";
  zone.dataset.index = String(index);

  const img = document.createElement("img");
  img.classList.add("hidden");

  const tip = document.createElement("span");
  tip.textContent = "点击 / 粘贴";

  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.classList.add("hidden");

  const remove = document.createElement("button");
  remove.type = "button";
  remove.className = "remove";
  remove.textContent = "×";

  zone.append(img, tip, input, remove);

  function setFile(file) {
    state.imageFiles[index] = file || null;
    if (file) {
      img.src = URL.createObjectURL(file);
      img.classList.remove("hidden");
      tip.classList.add("hidden");
      zone.classList.remove("empty");
    } else {
      img.classList.add("hidden");
      tip.classList.remove("hidden");
      zone.classList.add("empty");
    }
    syncAddButton();
  }

  zone.addEventListener("click", (e) => {
    if (e.target === remove) return;
    input.click();
  });
  input.addEventListener("change", () => setFile(input.files[0]));
  remove.addEventListener("click", (e) => {
    e.stopPropagation();
    input.value = "";
    setFile(null);
  });
  zone.addEventListener("dragover", (e) => {
    e.preventDefault();
    zone.classList.add("dragover");
  });
  zone.addEventListener("dragleave", () => zone.classList.remove("dragover"));
  zone.addEventListener("drop", (e) => {
    e.preventDefault();
    zone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) setFile(file);
  });

  state.imageFiles[index] = null;
  el.imagesBox.append(zone);
  syncAddButton();
}

function syncAddButton() {
  if (!state.selected) return;
  const used = state.imageFiles.filter(Boolean).length;
  const max = state.selected.max_images;
  for (const zone of el.imagesBox.querySelectorAll(".dropzone.empty")) {
    if (!zone.dataset.index) {
      zone.classList.toggle("hidden", used >= max);
    }
  }
}

function fillFirstEmptyImage(file) {
  const zone = Array.from(el.imagesBox.querySelectorAll(".dropzone")).find(
    (z) => z.classList.contains("empty") && z.dataset.index
  );
  if (zone) {
    const input = zone.querySelector("input");
    const view = new DataTransfer();
    view.items.add(file);
    input.files = view.files;
    input.dispatchEvent(new Event("change"));
    return true;
  }
  return false;
}

function buildTextInputs(meme) {
  el.textsBox.innerHTML = "";
  const { min_texts: minTexts, max_texts: maxTexts, default_texts: defaultTexts } = meme;

  if (maxTexts <= 0) {
    el.textsArea.classList.add("hidden");
    state.textCount = 0;
    return;
  }
  el.textsArea.classList.remove("hidden");
  el.textsHint.textContent = `需要 ${rangeText(minTexts, maxTexts)}`;

  state.textCount = minTexts;
  for (let i = 0; i < minTexts; i++) {
    addTextRow((defaultTexts && defaultTexts[i]) || "", minTexts, maxTexts);
  }
  addRemainingHint(minTexts, maxTexts);
}

function addTextRow(value, minTexts, maxTexts) {
  const row = document.createElement("div");
  row.className = "text-row";

  const input = document.createElement("input");
  input.type = "text";
  input.value = value;
  input.placeholder = "输入文字";
  row.append(input);

  if (state.textCount > minTexts) {
    const del = document.createElement("button");
    del.type = "button";
    del.className = "icon-btn";
    del.textContent = "−";
    del.addEventListener("click", () => {
      row.remove();
      state.textCount--;
      addRemainingHint(minTexts, maxTexts);
    });
    row.append(del);
  }
  el.textsBox.append(row);
}

function addRemainingHint(minTexts, maxTexts) {
  if (state.textCount >= maxTexts) return;
  if (el.textsBox.querySelector(".add-text")) return;
  const add = document.createElement("button");
  add.type = "button";
  add.className = "ghost add-text";
  add.textContent = "+ 添加文字";
  add.style.alignSelf = "flex-start";
  add.addEventListener("click", () => {
    if (state.textCount >= maxTexts) return;
    state.textCount++;
    addTextRow("", minTexts, maxTexts);
    addRemainingHint(minTexts, maxTexts);
    if (state.textCount >= maxTexts) add.remove();
  });
  el.textsBox.append(add);
}

/* ---------------- 选择与详情 ---------------- */

function selectMeme(key) {
  const meme = state.memes.find((m) => m.key === key);
  if (!meme) return;

  state.selected = meme;
  highlightActive();
  setStatus("");
  el.resultBox.classList.add("hidden");
  el.placeholder.classList.add("hidden");
  el.detail.classList.remove("hidden");

  el.dKey.textContent = meme.key;
  el.dKeywords.innerHTML = "";
  for (const k of meme.keywords) {
    el.dKeywords.append(chip(k, false));
  }

  el.dMeta.innerHTML = "";
  if (meme.max_images > 0)
    el.dMeta.append(chip(`图片 ${rangeText(meme.min_images, meme.max_images)}`, true));
  if (meme.max_texts > 0)
    el.dMeta.append(chip(`文字 ${rangeText(meme.min_texts, meme.max_texts)}`, true));
  for (const tag of meme.tags) el.dMeta.append(chip(tag, true));

  el.dPreview.src = `/memes/${encodeURIComponent(meme.key)}/preview`;

  buildImageSlots(meme);
  buildTextInputs(meme);
}

function chip(text, gray) {
  const span = document.createElement("span");
  span.className = gray ? "chip gray" : "chip";
  span.textContent = text;
  return span;
}

/* ---------------- 生成 ---------------- */

function setStatus(text, isError) {
  el.status.textContent = text;
  el.status.classList.toggle("error", !!isError);
}

function extOf(mime) {
  if (mime === "image/gif") return "gif";
  if (mime === "image/jpeg") return "jpg";
  if (mime === "image/webp") return "webp";
  return "png";
}

async function generate() {
  const meme = state.selected;
  if (!meme) return;

  const form = new FormData();
  const images = state.imageFiles.filter(Boolean);
  if (images.length < meme.min_images) {
    setStatus(`至少需要 ${meme.min_images} 张图片`, true);
    return;
  }
  for (const file of images) form.append("images", file, file.name || "image.png");

  const texts = Array.from(el.textsBox.querySelectorAll("input"))
    .map((input) => input.value)
    .filter((text) => text.trim() !== "");
  if (texts.length < meme.min_texts) {
    setStatus(`至少需要 ${meme.min_texts} 条文字`, true);
    return;
  }
  for (const text of texts) form.append("texts", text);
  form.append("args", JSON.stringify({ user_infos: [] }));

  el.generateBtn.disabled = true;
  setStatus("生成中…");
  el.resultBox.classList.add("hidden");

  try {
    const res = await fetch(`/memes/${encodeURIComponent(meme.key)}/`, {
      method: "POST",
      body: form,
    });
    if (!res.ok) {
      let detail = `${res.status}`;
      try {
        const data = await res.json();
        detail = data.detail || detail;
      } catch (e) {
        /* 保持默认错误信息 */
      }
      throw new Error(detail);
    }
    const blob = await res.blob();
    showResult(blob, meme.key);
    setStatus("生成成功");
  } catch (err) {
    setStatus(err.message || "生成失败", true);
  } finally {
    el.generateBtn.disabled = false;
  }
}

function showResult(blob, key) {
  if (el.resultImg.dataset.url) URL.revokeObjectURL(el.resultImg.dataset.url);
  const url = URL.createObjectURL(blob);
  el.resultImg.src = url;
  el.resultImg.dataset.url = url;
  el.downloadBtn.href = url;
  el.downloadBtn.download = `${key}.${extOf(blob.type)}`;
  el.resultBox.classList.remove("hidden");
}

/* ---------------- 事件绑定 ---------------- */

let searchTimer = null;
el.search.addEventListener("input", () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(renderList, 200);
});

el.previewSwitch.addEventListener("change", () => {
  previewQueue.clear();
  for (const item of el.memeList.children) {
    if (el.previewSwitch.checked) {
      requestPreview(item);
    } else {
      cancelPreview(item);
      const img = item.querySelector("img");
      if (img && img.src) {
        if (img.dataset.url) URL.revokeObjectURL(img.dataset.url);
        img.removeAttribute("src");
      }
    }
  }
});

el.randomBtn.addEventListener("click", () => {
  if (!state.memes.length) return;
  const meme = state.memes[Math.floor(Math.random() * state.memes.length)];
  selectMeme(meme.key);
  const item = el.memeList.querySelector(`[data-key="${CSS.escape(meme.key)}"]`);
  if (item) item.scrollIntoView({ block: "nearest" });
});

el.generateBtn.addEventListener("click", generate);

document.addEventListener("paste", (e) => {
  if (!state.selected) return;
  const item = Array.from(e.clipboardData.items).find((i) =>
    i.type.startsWith("image/")
  );
  if (!item) return;
  const file = item.getAsFile();
  if (!file) return;
  file.name = file.name || "pasted.png";
  if (!fillFirstEmptyImage(file)) setStatus("没有可用的图片位置了", true);
});

/* ---------------- 初始化 ---------------- */

async function init() {
  try {
    const res = await fetch("/api/memes");
    state.memes = await res.json();
    renderList();
  } catch (err) {
    el.count.textContent = "表情列表加载失败";
  }
  try {
    const res = await fetch("/meme/version");
    el.version.textContent = `v${(await res.text()).replace(/"/g, "")}`;
  } catch (err) {
    /* 忽略版本号获取失败 */
  }
}

init();
