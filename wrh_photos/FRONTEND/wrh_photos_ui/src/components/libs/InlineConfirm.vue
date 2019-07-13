<template>

  <span>
    <button type="button" v-show="!confirm" @click.prevent="confirm=!confirm" :class="btnClass" :disabled="disabled? 'disabled':false">
        <slot></slot>
    </button>
    <span v-show="confirm" :class="sureClass">
    {{ sureText }}
    </span>
    <button type="button" v-show="confirm" class="btn" @click.prevent="triggerConfirmed" :class="yesClass"
            :disabled="confirming">
      <span v-show="!confirming"><span :class="yesIconClass"></span> {{ yesText }}</span>
      <span v-show="confirming"><span :class="confirmingIconClass"></span> {{ confirmingText }}</span>
    </button>
    <button type="button" v-show="confirm" class="btn" @click.prevent="confirm=!confirm" :class="noClass">
      <span :class="noIconClass"></span> {{ noText }}
    </button>
  </span>

</template>

<script>
export default {
  props: {
    btnClass: String,
    sureClass: String,
    yesClass: String,
    noClass: String,
    disabled: Boolean,
    yesIconClass: String,
    noIconClass: String,
    confirmingIconClass: String,
    record: Object,
    confirming: {
      type: Boolean,
      default: false
    },
    yesText: {
      type: String,
      default: "Yes"
    },
    noText: {
      type: String,
      default: "No"
    },
    sureText: {
      type: String,
      default: "Sure?"
    },
    confirmingText: {
      type: String,
      default: ""
    }
  },
  data: function() {
    return {
      confirm: false
    };
  },
  methods: {
    triggerConfirmed: function() {
      this.$emit("confirmed", this.record, this);
    },
    hideConfirm: function() {
      this.confirm = false;
    }
  }
};
</script>
