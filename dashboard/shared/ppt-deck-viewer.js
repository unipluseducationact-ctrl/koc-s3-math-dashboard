/* Full PowerPoint video export viewer — one MP4 per deck folder. */
(function () {
  "use strict";
  var body = document.body;
  var title = body.getAttribute("data-ppt-title") || "Lesson deck";
  var videoFile = body.getAttribute("data-ppt-video") || "main.mp4";

  document.title = title;
  body.innerHTML =
    '<div class="bar">' +
      '<span class="title">' + title + "</span>" +
      '<span class="meta" id="meta"></span>' +
      '<button type="button" id="play-btn">Play / Pause</button>' +
      '<button type="button" id="restart-btn">Restart</button>' +
    "</div>" +
    '<div class="stage" id="stage">' +
      '<video id="v" src="' + videoFile + '" controls playsinline preload="metadata"></video>' +
    "</div>";

  var v = document.getElementById("v");
  var stage = document.getElementById("stage");
  var meta = document.getElementById("meta");
  var failed = false;

  function showError(msg) {
    if (failed) return;
    failed = true;
    stage.innerHTML =
      '<div class="err"><strong>Video not ready</strong>' + msg +
      "<br><br>In PowerPoint: <b>File → Export → Create a Video</b>, save as " +
      "<code>" + videoFile + "</code> in this folder, then refresh.</div>";
  }

  v.addEventListener("error", function () {
    showError("Could not load <code>" + videoFile + "</code> (missing, locked, or 0 bytes).");
  });
  v.addEventListener("loadedmetadata", function () {
    if (!v.duration || !isFinite(v.duration)) {
      showError("Video file appears empty — re-export from PowerPoint.");
      return;
    }
    var mins = Math.floor(v.duration / 60);
    var secs = Math.round(v.duration % 60);
    meta.textContent = mins + "m " + secs + "s";
  });

  document.getElementById("play-btn").addEventListener("click", function () {
    if (failed) return;
    if (v.paused) v.play(); else v.pause();
  });
  document.getElementById("restart-btn").addEventListener("click", function () {
    if (failed) return;
    v.currentTime = 0;
    v.play();
  });

  window.addEventListener("keydown", function (e) {
    if (failed) return;
    if (e.key === " " || e.key === "Spacebar") {
      e.preventDefault();
      if (v.paused) v.play(); else v.pause();
    }
    if (e.key === "ArrowRight") { e.preventDefault(); v.play(); }
    if (e.key === "ArrowLeft") {
      e.preventDefault();
      v.currentTime = Math.max(0, v.currentTime - 5);
    }
  });

  window.Reveal = {
    isReady: function () { return !failed; },
    slide: function () {},
    getIndices: function () { return { h: 0, v: 0, f: 0 }; },
  };
})();
