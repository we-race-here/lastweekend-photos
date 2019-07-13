import { Config } from "../../Config";
import $ from "jquery";

const moment = window.moment;

moment.updateLocale("en", {
  relativeTime: {
    s: "Just now",
    ss: "Just now",
    m: "1 min",
    mm: "%d mins",
    h: "1 hr",
    hh: "%d hrs"
  }
});

export default {
  mixins: [Config],
  methods: {
    getTimeLabel: function(hour, minute, baseHour) {
      var mer = "AM";
      hour = (hour + (baseHour === undefined ? 21 : baseHour)) % 24;
      if (hour === 0) {
        hour = 12;
      }
      if (hour > 12) {
        mer = "PM";
        hour = hour % 12;
      }
      hour = `${hour}`.padStart(2, "0");
      if (minute === undefined) {
        return `${hour} ${mer}`;
      }
      minute = `${minute}`.padStart(2, "0");
      return `${hour}:${minute} ${mer}`;
    },
    todayDate: function(options) {
      options = options || {};
      if (options.asDate) {
        return moment().toDate();
      }
      return moment().format(options.format || "YYYY-MM-DD");
    },
    formatDate: function(value, fmt, _default) {
      _default = _default === undefined ? "" : _default;
      if (!value) {
        return _default;
      }
      fmt = fmt === undefined ? "MMM D, YYYY HH:mm" : fmt;
      return moment(value).format(fmt);
    },
    formatTime: function(value, fmt, _default) {
      _default = _default === undefined ? "" : _default;
      if (!value) {
        return _default;
      }
      fmt = fmt === undefined ? "hh:mm A" : fmt;
      return moment.utc(`2000-01-01T${value}Z`).format(fmt);
    },
    formatDefault: function(value, _default) {
      return value === null || value === undefined || value === ""
        ? _default
        : value;
    },
    formatBoolean: function(value) {
      return `<span class="la la-${
        value ? "check text-success" : "close text-danger"
      }"></span>`;
    },
    formatFileUrl: function(fileUrl) {
      return fileUrl
        .split("?")[0]
        .split("/")
        .pop();
    },
    formatDuration: function(d, includeSeconds, _default) {
      d = d || 0;
      if (!d && _default !== undefined) {
        return _default;
      }
      var hours = Math.floor(d / 3600),
        minutes = Math.floor((d % 3600) / 60);
      var s = `${hours}<sub>h</sub> : ${minutes}<sub>m</sub>`;
      if (includeSeconds) {
        var seconds = Math.floor((d % 3600) % 60);
        s = `${s}: ${seconds}<sub>s</sub>`;
      }
      return s;
    },
    formatDuration2: function(d, includeSeconds, _default) {
      d = d || 0;
      if (!d && _default !== undefined) {
        return _default;
      }
      var hours = Math.floor(d / 3600),
        minutes = Math.floor((d % 3600) / 60);
      var s = `${hours}:${minutes}`;
      if (includeSeconds) {
        var seconds = Math.floor((d % 3600) % 60);
        s = `${s}: ${seconds}`;
      }
      return s;
    },
    formatFileType: function(fileUrl, showText, showIcon) {
      if (!fileUrl) {
        return "";
      }
      showText = showText === undefined ? true : showText;
      showIcon = showIcon === undefined ? true : showIcon;
      var ext = fileUrl
          .split(".")
          .slice(-1)[0]
          .toLowerCase(),
        extTypes = {
          jpg: "image",
          jpeg: "image",
          png: "image",
          gif: "image",
          pdf: "pdf",
          doc: "word",
          docx: "word",
          xls: "excel",
          xlsx: "excel",
          csv: "excel",
          zip: "zip",
          tar: "zip",
          "7z": "zip",
          bz2: "zip",
          gz: "zip",
          tgz: "zip"
        },
        icons = {
          image: "fa-file-image-o",
          pdf: "fa-file-pdf-o",
          word: "fa-file-word-o",
          excel: "fa-file-excel-o",
          zip: "fa-file-zip-o",
          unknown: "fa-file-o"
        },
        extType = extTypes[ext] || "unknown",
        icon = icons[extType];
      var s = "";
      if (showIcon) {
        s += `<span class="fa ${icon}"></span> `;
      }
      if (showText) {
        s += extType;
      }
      return s;
    },
    ifEmptyFormat: function(value, _default) {
      return value || (_default || "-");
    },
    formatFileSize: function(value, _default) {
      _default = _default === undefined ? "" : _default;
      const UNITS = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
      if (value === null || value === undefined) {
        return _default;
      }
      if (!Number.isFinite(value)) {
        throw new TypeError("Expected a finite number");
      }
      const neg = value < 0;
      if (neg) {
        value = -value;
      }
      if (value < 1) {
        return (neg ? "-" : "") + value + " B";
      }
      const exponent = Math.min(
        Math.floor(Math.log10(value) / 3),
        UNITS.length - 1
      );
      const valueStr = Number(
        (value / Math.pow(1000, exponent)).toPrecision(3)
      );
      const unit = UNITS[exponent];
      return (neg ? "-" : "") + valueStr + " " + unit;
    },
    capitalize: function(value) {
      if (!value) return "";
      value = value.toString();
      return value.charAt(0).toUpperCase() + value.slice(1);
    },
    ageFormat: function(birth_date, showLabel) {
      showLabel = showLabel === undefined ? true : showLabel;
      return `${moment().diff(birth_date, "years")}${
        showLabel ? " years" : ""
      }`;
    },
    removeTrailingZero: function(n, decimalPoint) {
      if (typeof n === "number" && decimalPoint !== undefined) {
        n = n.toFixed(decimalPoint);
      }
      if (typeof n !== "string") {
        n = n + "";
      }
      return n.replace(/(\.[0-9]*[1-9])0+$|\.0*$/, "$1");
    },
    findIndexBy: function(array, property, value) {
      for (var i = 0; i < array.length; i++) {
        if (array[i][property] === value) {
          return i;
        }
      }
      return -1;
    },
    findValueBy: function(array, property, value) {
      for (var i = 0; i < array.length; i++) {
        if (array[i][property] === value) {
          return array[i];
        }
      }
    },
    getCookie: function(cName) {
      if (document.cookie.length > 0) {
        var cStart = document.cookie.indexOf(cName + "=");
        if (cStart !== -1) {
          cStart = cStart + cName.length + 1;
          var cEnd = document.cookie.indexOf(";", cStart);
          if (cEnd === -1) {
            cEnd = document.cookie.length;
          }
          return encodeURI(document.cookie.substring(cStart, cEnd));
        }
      }
      return "";
    },
    closeAllNotify: function() {
      $.notifyClose();
    },
    showMessage: function(msg, opts) {
      opts = Object.assign(
        {
          element: "body", // which element to append to
          type: "info", // (null, 'info', 'danger', 'success')
          offset: { y: 20 }, // {x: 20, y: 20}
          placement: { align: "center" },
          newest_on_top: true,
          width: "auto", // (integer, or 'auto')
          timer: 5000, // Time while the message will be displayed. It's not equivalent to the *demo* timeOut!
          z_index: 9999999,
          allow_dismiss: true // If true then will display a cross to close the popup.
        },
        opts || {}
      );
      $.notify(msg, opts);
    },
    showSuccess: function(msg, delay) {
      this.showMessage(msg, {
        type: "success",
        timer: delay !== undefined ? delay : 5000
      });
    },
    showError: function(msg, delay) {
      this.showMessage(msg, {
        type: "danger",
        timer: delay !== undefined ? delay : 5000
      });
    },
    showWarn: function(msg, delay) {
      this.showMessage(msg, {
        type: "warning",
        timer: delay !== undefined ? delay : 5000
      });
    },
    showInfo: function(msg, delay) {
      this.showMessage(msg, {
        type: "info",
        timer: delay !== undefined ? delay : 5000
      });
    },
    showDefaultServerSuccess: function(response, delay) {
      delay = delay !== undefined ? delay : 5000;
      var defaultMsg = "Operation done successfully";
      this.showSuccess(response.statusText || defaultMsg, delay);
    },
    showDefaultServerError: function(error, showReason, delay, extra_message) {
      var response = error.response || error.request;
      if (response.status === 401) {
        return;
      }
      var msg;
      delay = delay !== undefined ? delay : 5000;
      showReason = showReason !== undefined ? showReason : true;
      if (!response || response.status <= 0) {
        msg = "<strong>Server Connection Error</strong>";
      } else {
        msg =
          "<strong>" +
          response.status +
          ": " +
          response.statusText +
          "</strong>";
        var jData = this.safeFromJson(response.data);
        if (showReason && jData) {
          msg += "<p>" + this.prettifyError(response.data) + "</p>";
        }
        if (extra_message) {
          msg += "<p>" + extra_message + "</p>";
        }
      }
      this.showError(msg, delay);
    },
    prettifyError: function(data) {
      return JSON.stringify(data)
        .replace(/\[|\]|\}|\{/g, "")
        .replace(/\\"/g, '"')
        .replace('"non_field_errors":', "");
    },
    safeFromJson: function(s, nullIfFail) {
      if (typeof s === "object") {
        return s;
      }
      nullIfFail = nullIfFail === undefined;
      try {
        return JSON.parse(s);
      } catch (e) {
        return nullIfFail ? null : s;
      }
    },
    randomId: function(n) {
      n = n || 10;
      return Math.floor(Math.random() * Math.pow(10, n) + 1);
    },
    addQSParm: function(url, name, value, override) {
      override = override === undefined ? true : override;
      var self = this;
      if (value instanceof Array) {
        $.each(value, function(k, v) {
          url = self.addQSParm(url, name, v, false);
        });
        return url;
      }
      var re = new RegExp("([?&]" + name + "=)[^&]+", "");

      function add(sep) {
        url += sep + name + "=" + encodeURIComponent(value);
      }

      function change() {
        url = url.replace(re, "$1" + encodeURIComponent(value));
      }

      if (url.indexOf("?") === -1) {
        add("?");
      } else {
        if (override && re.test(url)) {
          change();
        } else {
          add("&");
        }
      }
      return url;
    },
    noCacheUrl: function(url) {
      var r = this.randomId();
      return this.addQSParm(url, "nc", r);
    },
    combineURLs: function(baseURL, relativeURL) {
      return (
        baseURL.replace(/\/+$/, "") + "/" + relativeURL.replace(/^\/+/, "")
      );
    },
    download: function downloadURL(url, params) {
      var self = this;
      $.each(params, function(k, v) {
        url = self.addQSParm(url, k, v);
      });
      var hiddenIFrameID = "hiddenDownloader",
        iframe = document.getElementById(hiddenIFrameID);
      if (iframe === null) {
        iframe = document.createElement("iframe");
        iframe.id = hiddenIFrameID;
        iframe.style.display = "none";
        document.body.appendChild(iframe);
      }
      iframe.src = url;
    },
    download2: function downloadURL(url, params) {
      var self = this;
      $.each(params, function(k, v) {
        url = self.addQSParm(url, k, v);
      });
      var hiddenLinkID = "hiddenLink",
        link = document.getElementById(hiddenLinkID);
      if (link === null) {
        link = document.createElement("a");
        link.target = "_blank";
        link.id = hiddenLinkID;
        link.style.display = "none";
        document.body.appendChild(link);
      }
      link.href = url;
      link.click();
    },
    convertModelToFormData: function(model, form, namespace, filter) {
      var formData = form || new FormData();
      var formKey;
      filter = filter === undefined ? k => k.startsWith("_") : filter;

      for (var propertyName in model) {
        if (
          !model.hasOwnProperty(propertyName) ||
          model[propertyName] === undefined ||
          (filter && filter(propertyName))
        ) {
          continue;
        }
        formKey = namespace || propertyName;
        if (model[propertyName] === null) {
          formData.append(formKey, "");
        } else if (model[propertyName] instanceof Date) {
          formData.append(formKey, model[propertyName].toISOString());
        } else if (model[propertyName] instanceof File) {
          formData.append(formKey, model[propertyName]);
        } else if (typeof model[propertyName] === "object") {
          this.convertModelToFormData(
            model[propertyName],
            formData,
            formKey,
            filter
          );
        } else {
          formData.append(formKey, model[propertyName].toString());
        }
      }
      return formData;
    },
    stripTags: function(value) {
      return $(`<span>${value}</span>`).text();
    }
  }
};
