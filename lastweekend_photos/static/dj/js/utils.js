function dateTimePickerWidget(inputId, options) {
  var $input = $("#" + inputId),
    containerId = "div_" + inputId,
    $container = $input.parent(),
    $addon = $input.next();
  $container.attr("id", containerId).attr("data-target-input", "nearest");
  $input.addClass("datetimepicker-input").attr("data-target", "#" + containerId);
  $addon.attr("data-toggle", "datetimepicker").attr("data-target", "#" + containerId);
  $("#" + containerId).datetimepicker(options);
}
