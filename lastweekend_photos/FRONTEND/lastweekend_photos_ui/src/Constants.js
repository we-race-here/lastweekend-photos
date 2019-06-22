export const UI_VERSION_HEADER_NAME = "x-ui-version";

export const GENDER_OPTIONS = [
  { value: "m", title: "Male" },
  { value: "f", title: "Female" },
  { value: "o", title: "Other" },
  { value: "u", title: "Unknown" }
];
export const GENDER_MAP = {};
GENDER_OPTIONS.forEach(function(v) {
  GENDER_MAP[v.value] = v;
});


export const LOGO_POSITION_OPTIONS = [
  {value: 'tl', title: 'Top-Left'},
  {value: 'tc', title: 'Top-Center'},
  {value: 'tr', title: 'Top-Right'},
  {value: 'cl', title: 'Center-Left'},
  {value: 'cc', title: 'Center-Center'},
  {value: 'cr', title: 'Center-Right'},
  {value: 'bl', title: 'Bottom-Left'},
  {value: 'bc', title: 'Bottom-Center'},
  {value: 'br', title: 'Bottom-Right'}
];
export const LOGO_POSITION_MAP = {};
LOGO_POSITION_OPTIONS.forEach(function(v) {
  LOGO_POSITION_MAP[v.value] = v;
});
