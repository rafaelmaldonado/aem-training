document.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-copy-slide]");
  if (!button) return;

  const slide = button.closest(".web-slide");
  const status = slide.querySelector("[data-copy-status]");
  const source = slide.dataset.slideSrc;
  button.disabled = true;
  status.textContent = "Preparing 3200 × 1800 image…";

  try {
    const svg = await fetch(source).then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.blob();
    });
    const url = URL.createObjectURL(svg);
    const image = new Image();
    await new Promise((resolve, reject) => {
      image.onload = resolve;
      image.onerror = reject;
      image.src = url;
    });
    const canvas = document.createElement("canvas");
    canvas.width = 3200;
    canvas.height = 1800;
    canvas.getContext("2d").drawImage(image, 0, 0, canvas.width, canvas.height);
    URL.revokeObjectURL(url);
    const png = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
    await navigator.clipboard.write([new ClipboardItem({ "image/png": png })]);
    status.textContent = "Copied. Paste directly into PowerPoint.";
  } catch (error) {
    status.textContent = "Copy failed. Download the slide image and insert it into PowerPoint.";
  } finally {
    button.disabled = false;
  }
});
