/**
 * jquery.goTop 返回顶部插件 v0.1
 * 作者：nekoleamo
 */
;
(function ($, window, document) {
    // noinspection Annotator
    $.fn.goTop = function (options) {
        const defaults = {
            scrollTop: 100,
            scrollSpeed: 1000,
            fadeInSpeed: 1000,
            fadeOutSpeed: 500
        };
        // noinspection Annotator
        // noinspection ES6ConvertVarToLetConst
        // noinspection ES6ConvertVarToLetConst
        // noinspection Annotator
        var options = $.extend(defaults, options);
        const $this = $(this);
        $(window).on('scroll', function () {
            // noinspection JSValidateTypes
            if ($(window).scrollTop() > options.scrollTop) {
                $this.fadeIn(options.fadeInSpeed);
            } else {
                $this.fadeOut(options.fadeOutSpeed);
            }
        });
        $this.on('click', function () {
            $('html,body').animate({
                'scrollTop': 0
            }, options.speed)
        })
    }
})(jQuery, window, document);