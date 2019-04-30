/******* Vue Filters ******/
import Vue from "vue";
import $ from "jquery";

Vue.filter("capitalize", function(value) {
  if (!value) return "";
  value = value.toString();
  return value.charAt(0).toUpperCase() + value.slice(1);
});

Vue.filter("stripTags", function(value) {
  if (!value) return "";
  return $(`<span>${value}</span>`).text();
  //return value.replace(/<.+?>/g, "");
});

Vue.filter("truncate", function(text, length, suffix) {
  length = length === undefined ? 50 : length;
  suffix = suffix === undefined ? "..." : suffix;
  return (
    (text || "").substring(0, length) + (length < text.length ? suffix : "")
  );
});
