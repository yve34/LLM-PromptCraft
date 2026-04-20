$(function () {
    if (ANSWERED) return;

    var $checkBtn = $('#check-btn');

    /* ── single_choice ─────────────────────────────────────────────── */
    if (QUESTION_TYPE === 'single_choice') {
        $(document).on('click', '.pc-quiz-option', function () {
            $('.pc-quiz-option').removeClass('selected');
            $(this).addClass('selected');
            $(this).find('.quiz-radio').prop('checked', true);
            $checkBtn.prop('disabled', false).removeClass('disabled');
        });
    }

    /* ── match ─────────────────────────────────────────────────────── */
    if (QUESTION_TYPE === 'match') {
        function refreshMatchState() {
            var selects = $('.pc-match-select');
            var values  = selects.map(function () { return $(this).val(); }).get();

            // Warn on duplicate sentence selections
            var seen = {};
            selects.each(function () {
                var v = $(this).val();
                if (!v) return;
                $(this).toggleClass('is-invalid', !!seen[v]);
                seen[v] = true;
            });

            var allFilled   = values.every(function (v) { return v !== '' && v !== null; });
            var noDupes     = Object.keys(seen).length === values.filter(Boolean).length;
            $checkBtn.prop('disabled', !(allFilled && noDupes));
        }

        $('.pc-match-select').on('change', refreshMatchState);
    }
});
