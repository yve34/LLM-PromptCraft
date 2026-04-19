/* PromptCraft — jQuery interactions.
   Only Lesson 5 needs JS (Build-A-Prompt interactive picker). Everything
   else is server-rendered. */

$(function () {

    /* ---------- Lesson 5: Build-A-Prompt ---------- */
    var $buildBoard = $('#build-prompt-board');
    if ($buildBoard.length === 0) return;

    var selections = {}; // {role: "A"|"B", context: ..., task: ..., format: ...}

    $buildBoard.on('click', '.pc-build-option', function () {
        var $opt = $(this);
        var key  = $opt.data('key');
        var id   = $opt.data('id');
        selections[key] = id;

        // visually mark selected + clear siblings in same row
        $buildBoard.find('.pc-build-option[data-key="' + key + '"]').removeClass('selected');
        $opt.addClass('selected');

        // enable assemble button once all 4 rows chosen
        if (Object.keys(selections).length === 4) {
            $('#assemble-btn').prop('disabled', false).removeClass('disabled');
        }
    });

    $('#assemble-btn').on('click', function (e) {
        e.preventDefault();
        if (Object.keys(selections).length < 4) return;

        // POST to backend — stores user choices (HW10 requirement #4)
        $.ajax({
            url: '/api/build-prompt',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ selections: selections })
        });

        // Render assembled prompt from the JSON we embedded in the DOM
        var $assembled = $('#assembled-prompt');
        $assembled.find('.row-item').each(function () {
            var $row = $(this);
            var key  = $row.data('key');
            var pick = selections[key];
            var text = $row.find('.opt-text[data-id="' + pick + '"]').text();
            $row.find('.final-text').text(text);
        });
        $assembled.addClass('visible');

        // Reveal the "Take the Quiz" CTA
        $('#take-quiz-cta').removeClass('d-none');

        // Scroll to the assembled view
        $('html, body').animate({
            scrollTop: $assembled.offset().top - 80
        }, 400);
    });
});
