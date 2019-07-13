<template>
  <input ref="inputText" type="text" :placeholder="placeholder" class="form-control m-input"/>
</template>

<script>
  import "jquery-datetimepicker";

  require("jquery-datetimepicker/jquery.datetimepicker.css");

  const jQuery = window.jQuery;
  const moment = window.moment;
  const events = [
    "onSelectTime",
    "onChangeMonth",
    "onChangeYear",
    "onShow",
    "onClose",
    "onSelectDate",
    "onGenerate"
  ];
  const isSafariBrowser = /^((?!chrome|android).)*safari/i.test(
      navigator.userAgent
  );

  jQuery.datetimepicker.setDateFormatter("moment");

  export default {
    name: "dateTime",
    props: {
      value: {
        default: null,
        required: true,
        validator: function validator(value) {
          return (
              value === null ||
              value instanceof Date ||
              typeof value === "string" ||
              value instanceof String ||
              value instanceof moment
          );
        }
      },
      config: {
        type: Object,
        default: function _default() {
          return {};
        }
      },
      wrap: {
        type: Boolean,
        default: false
      },
      timeonly: {
        type: Boolean,
        default: false
      },
      comparator: {
        // options: 'format', 'date', 'time', CUSTOM_FORMAT
        type: String,
        default: "format"
      },
      placeholder: {
        type: String,
        default: ""
      },
    },
    data: function data() {
      return {
        elem: null
      };
    },
    mounted: function () {
      this.elem = jQuery(this.$el);
      if (this.value) {
        if (this.timeonly && typeof this.value === "string") {
          this.config.value = this.timeStrToDate(this.value);
        } else {
          this.config.value = moment(this.value).toDate();
        }
      }
      if (isSafariBrowser) {
        this.config.mask = false; // TODO: we have a auto focus bug in safari browser when mask is enabled!
      }
      this.elem.datetimepicker(this.config);
      this.elem.datetimepicker({onChangeDateTime: this.onChange});
      if (this.wrap) {
        var self = this;
        jQuery(
            this.config.iconRef || ".input-group-addon",
            this.$el.parentNode
        ).on("click", function () {
          self.elem.focus();
        });
      }
      this.registerEvents();
    },

    watch: {
      value: function value(value) {
        if (this.timeonly && typeof value === "string") {
          value = this.timeStrToDate(value);
        }
        this.elem.datetimepicker({
          value: value ? moment(value).toDate() : value
        });
        if (!value) {
          this.$el.value = value;
        }
      },
      config: {
        deep: true,
        handler: function handler(newConfig) {
          if (isSafariBrowser) {
            newConfig.mask = false; // TODO: we have a auto focus bug in safari browser when mask is enabled!
          }
          this.elem.datetimepicker(newConfig);
        }
      }
    },
    methods: {
      timeStrToDate: function (time) {
        var splitedTime = time.split(":");
        return moment()
            .set({
              hour: (splitedTime[0] || 0) * 1,
              minute: (splitedTime[1] || 0) * 1,
              second: (splitedTime[2] || 0) * 1
            })
            .toDate();
      },
      onChange: function (value) {
        let momentValue = value && moment(value),
            oldMomentValue = null;
        if (this.timeonly) {
          value = value && momentValue.format("HH:mm:ss");
          if (this.value) {
            if (typeof this.value === "string") {
              var splitedTime = this.value.split(":");
              oldMomentValue = moment().set({
                hour: (splitedTime[0] || 0) * 1,
                minute: (splitedTime[1] || 0) * 1,
                second: (splitedTime[2] || 0) * 1
              });
            } else {
              oldMomentValue = moment(this.value);
            }
          }
        } else {
          value = value && momentValue.toDate();
          oldMomentValue = this.value && moment(this.value);
        }
        let comparatorFormat = this.comparator;
        if (this.comparator === "date") {
          comparatorFormat = "YYYY-MM-DD";
        } else if (this.comparator === "time") {
          comparatorFormat = "HH:mm";
        } else if (this.comparator === "format") {
          comparatorFormat = this.config.format;
        }
        if (
            (value && momentValue.format(comparatorFormat)) !==
            (this.value && oldMomentValue.format(comparatorFormat))
        ) {
          value = value && momentValue.format(comparatorFormat);
          this.$emit("input", value);
        }
      },
      registerEvents: function () {
        let self = this;
        events.forEach(function (name) {
          self.elem.datetimepicker({
            [name]: function () {
              for (
                  var _len = arguments.length, args = Array(_len), _key = 0;
                  _key < _len;
                  _key++
              ) {
                args[_key] = arguments[_key];
              }
              self.$emit.apply(self, [name.slice(2).toLowerCase()].concat(args));
            }
          });
        });
      }
    },
    beforeDestroy: function () {
      if (this.elem) {
        this.elem.datetimepicker("destroy");
        this.elem = null;
      }
    }
  };
</script>
