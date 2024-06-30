<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>

import axios from "axios";
import * as d3 from 'd3';
export default {
  name: 'App',
}
</script>

<style scope>
  #app {
    width: 100%;
    height: 100%;
    display: flex;
    background-color: #eef4f8;
  }
</style>

<style>
  @import "assets/css/base.css";
</style>
