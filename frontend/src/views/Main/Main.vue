<!--<template>-->
<!--  &lt;!&ndash; 界面左部分视图 &ndash;&gt;-->
<!--  <div class="LeftPart">-->
<!--    &lt;!&ndash; 查询输入部分 &ndash;&gt;-->
<!--    <div class="QueryInputPart">-->
<!--      <div class="QueryTaskInputPart FlexRow ColorBox">-->
<!--        <span>Query task</span>-->
<!--        <el-input class="QueryTaskInput" v-model="QueryTask"></el-input>-->
<!--      </div>-->

<!--      <div class="QueryInput ColorBox">-->
<!--        <div class="MainHeading">Query Input</div>-->

<!--        <div class="QueryInputBody FlexRow">-->
<!--          &lt;!&ndash; Important Attr Part &ndash;&gt;-->
<!--          <div class="IAPart QueryInputPart">-->
<!--            <div class="SubHeading">Important Attr Part</div>-->
<!--            <div class="IAItem">-->
<!--              {{ IA }}-->
<!--            </div>-->
<!--          </div>-->
<!--          &lt;!&ndash; Normal Attr Part &ndash;&gt;-->
<!--          <div class="NAPart QueryInputPart">-->
<!--            <div class="SubHeading">Normal Attr Part</div>-->
<!--            <div class="NABody">-->
<!--              <el-checkbox-->
<!--                v-for="column in DatasetColumns.filter((d) => d !== IA)"-->
<!--                :key="column"-->
<!--                v-model="NAMap[column]"-->
<!--                :label="column"-->
<!--                size="large"-->
<!--                class="NAItem"-->
<!--              />-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->

<!--      <div class="QueryListShow ColorBox">-->
<!--        <div class="MainHeading">Query List</div>-->
<!--        <div class="QueryListShowBody">-->
<!--          <el-radio-group v-model="CurShowQuery" class="ml-4">-->
<!--            <el-radio class="QueryListShowItem"-->
<!--                      v-for="query in QueryList"-->
<!--                      :label="query" size="large"-->
<!--                      :key="query"-->
<!--            >{{query}}</el-radio>-->
<!--          </el-radio-group>-->
<!--        </div>-->
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->

<!--  &lt;!&ndash; 界面中部分视图 &ndash;&gt;-->
<!--  <div class="MidPart">-->
<!--    &lt;!&ndash; 基本信息部分 &ndash;&gt;-->
<!--    <div class="QueryPreview ColorBox">-->
<!--      <div class="MainHeading">QueryPreview</div>-->
<!--      <div class="QueryPreviewBody">-->
<!--        <h2>CurQueryAttrList</h2>-->
<!--        <draggable v-model="CurQueryAttrList"-->
<!--                   group="attr"-->
<!--                   class="CurQueryAttrListPart">-->
<!--          <template #item="{element}">-->
<!--            <div>{{element}}</div>-->
<!--          </template>-->
<!--        </draggable>-->

<!--        <h2>DistributionAttr</h2>-->
<!--        <draggable v-model="DistributionAttr"-->
<!--                   group="attr"-->
<!--                   class="DistributionAttrPart">-->
<!--          <template #item="{element}">-->
<!--            <div>{{element}}</div>-->
<!--          </template>-->
<!--        </draggable>-->

<!--        <h2>QueryContent</h2>-->
<!--        <draggable v-model="QueryContent"-->
<!--                   group="attr"-->
<!--                   class="QueryContentPart">-->
<!--          <template #item="{element}">-->
<!--            <div>{{element}}</div>-->
<!--          </template>-->
<!--        </draggable>-->

<!--        <el-button type="primary" @click="QueryConfirm">Query</el-button>-->
<!--      </div>-->
<!--    </div>-->

<!--    &lt;!&ndash; 当前图展示部分 &ndash;&gt;-->
<!--    <div class="CurGraphShowPart ColorBox">-->
<!--      <div class="MainHeading">CurGraphShowPart</div>-->
<!--      <div class="CurGraphShowBody">-->
<!--        <svg class="CurGraph"></svg>-->
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->

<!--  <div class="RightPart">-->
<!--    &lt;!&ndash; 历史视图部分 &ndash;&gt;-->
<!--    <div class="HistoryGraphPart ColorBox">HistoryGraphPart</div>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import * as d3 from "d3";-->
<!--import draggable from 'vuedraggable';-->
<!--import axios from "axios";-->

<!--export default {-->
<!--  name: "Main",-->
<!--  components: {draggable},-->
<!--  data() {-->
<!--    return {-->
<!--      QueryTask: "",-->
<!--      NAMap: {}, // judge whether a na is included in the query group-->
<!--      CurShowQuery: '',-->
<!--      CurQueryAttrList: [],-->
<!--      DistributionAttr: [],-->
<!--      QueryContent: [],-->

<!--      Dataset: [],-->
<!--      DatasetColumns: [],-->
<!--      AttrTypeMap: [], // A: categorical  #: numerical  T: temporal-->
<!--      AttrRangeMap: [],-->

<!--      SvgWidth: 800,-->
<!--      SvgHeight: 400,-->


<!--    };-->
<!--  },-->
<!--  computed: {-->
<!--    IA() {-->
<!--      for (let column of this.DatasetColumns) {-->
<!--        if (this.QueryTask.includes(column)) {-->
<!--          return column;-->
<!--        }-->
<!--      }-->
<!--      return "";-->
<!--    },-->
<!--    QueryList() {-->
<!--      let NAL = Object.keys(this.NAMap).filter((d) => this.NAMap[d]);-->
<!--      if (this.IA === "") {-->
<!--        return NAL;-->
<!--      } else {-->
<!--        return NAL.map((d) => this.IA + "——" + d);-->
<!--      }-->
<!--    },-->
<!--    CurQuery() {-->
<!--      if (this.QueryList.length === 0) {-->
<!--        return "";-->
<!--      } else {-->
<!--        return this.QueryList[this.QueryList.length - 1];-->
<!--      }-->
<!--    },-->
<!--  },-->
<!--  watch: {-->
<!--    QueryList: {-->
<!--    handler(newVal, oldVal) {-->
<!--      if(newVal.length !== 0) {-->
<!--        this.CurShowQuery = newVal[newVal.length-1];-->
<!--      }-->
<!--    },-->
<!--      deep: false-->
<!--    },-->
<!--    CurQuery(newVal, oldVal) {-->
<!--      if(this.CurQuery === '') {-->
<!--        this.CurQueryAttrList = [];-->
<!--      }-->
<!--      else {-->
<!--        let CurQueryAttrList = this.CurQuery.split('——');-->
<!--        CurQueryAttrList.push('#COUNT');-->
<!--        this.CurQueryAttrList = CurQueryAttrList;-->
<!--      }-->
<!--    },-->
<!--    // CurShowQuery(newVal, oldVal) {-->
<!--    //   if (newVal === "") {-->
<!--    //   } else {-->
<!--    //     let CurQueryArray = newVal.split("——");-->
<!--    //     let QueryAttrs = [-->
<!--    //       {-->
<!--    //         name: CurQueryArray[0],-->
<!--    //       },-->
<!--    //     ];-->
<!--    //     let QueryContent =-->
<!--    //       CurQueryArray.length === 1 ? "#COUNT" : CurQueryArray[1];-->
<!--    //     // 执行查询-->
<!--    //     let [queryRes, axisAttr] = this.executeQuery(QueryAttrs, QueryContent);-->
<!--    //     // 绘制查询结果-->
<!--    //     this.drawQueryResult(queryRes, axisAttr);-->
<!--    //   }-->
<!--    // },-->
<!--  },-->
<!--  methods: {-->
<!--    // 接口类函数-->
<!--    // 执行查询接口-->
<!--    executeQuery(QueryAttrs, QueryContent) {-->
<!--      // 单属性 + COUNT 的情况-->
<!--      if (QueryAttrs.length === 1) {-->
<!--        let QueryAttrName = QueryAttrs[0].name;-->
<!--        let queryRes = this.getQueryRes(-->
<!--          QueryAttrName,-->
<!--          QueryContent,-->
<!--          this.Dataset-->
<!--        );-->
<!--        let axisAttr = [QueryAttrName, QueryContent];-->
<!--        return [queryRes[1], axisAttr];-->
<!--      }-->
<!--      // 双属性查询的情况-->
<!--      else {-->
<!--        let QueryAttrNames = [QueryAttrs[0].name, QueryAttrs[1].name];-->
<!--        let [bins, queryRes] = this.getQueryRes(-->
<!--          QueryAttrNames[0],-->
<!--          QueryContent,-->
<!--          this.Dataset-->
<!--        );-->
<!--        let axisAttr = [QueryAttrNames[0], QueryContent, QueryAttrNames[1]];-->
<!--        let binKeys = Object.keys(queryRes);-->
<!--        let secondDataDomain;-->
<!--        if (this.AttrTypeMap[QueryAttrNames[1]] === "#") {-->
<!--          secondDataDomain = [-->
<!--            d3.min(bins, (bin) => d3.min(bin, (d) => d[QueryAttrNames[1]])),-->
<!--            d3.max(bins, (bin) => d3.max(bin, (d) => d[QueryAttrNames[1]])),-->
<!--          ];-->
<!--        }-->

<!--        for (let idx in bins) {-->
<!--          let [, secondaQueryRes] = this.getQueryRes(-->
<!--            QueryAttrNames[1],-->
<!--            QueryContent,-->
<!--            bins[idx],-->
<!--            secondDataDomain-->
<!--          );-->
<!--          queryRes[binKeys[idx]] = secondaQueryRes;-->
<!--        }-->
<!--        return [queryRes, axisAttr];-->
<!--      }-->
<!--    },-->
<!--    // 绘制查询结果接口-->
<!--    drawQueryResult(queryRes, queryAttrs) {-->
<!--      let [SvgWidth, SvgHeight] = [this.SvgWidth, this.SvgHeight];-->
<!--      let padding = 70;-->
<!--      let yMax;-->
<!--      // 将 Map 数据转换为数组-->
<!--      const data = Object.entries(queryRes);-->
<!--      let isStack = typeof data[0][1] === 'object';-->
<!--      if(isStack) {-->
<!--        SvgWidth -= 200;-->
<!--      }-->
<!--      // 创建 SVG 元素-->
<!--      const svg = d3.select(".CurGraph");-->
<!--      svg.selectAll("*").remove();-->


<!--      let secondCategory;-->
<!--      if (typeof data[0][1] === "object") {-->
<!--        secondCategory = Object.keys(data[0][1]);-->
<!--        for (let d of data) {-->
<!--          d[1] = Object.entries(d[1]);-->
<!--        }-->
<!--        yMax = d3.max(data, ([category, value]) =>-->
<!--          d3.sum(value, ([c, v]) => v)-->
<!--        );-->
<!--      } else {-->
<!--        yMax = d3.max(data, ([category, value]) => value);-->
<!--      }-->

<!--      // 设置比例尺-->
<!--      let xDomain = data.map(([category, value]) => category);-->
<!--      let xScale;-->
<!--      let bandwidth;-->
<!--      let isNumerical = !isNaN(xDomain[0].split("-")[0]);-->
<!--      let tickValues = [];-->
<!--      if (isNumerical) {-->
<!--        // 数值型-->
<!--        let numericalDomain = [-->
<!--          Number(xDomain[0].split("-")[0]),-->
<!--          Number(xDomain[xDomain.length - 1].split("-")[1]),-->
<!--        ];-->
<!--        xScale = d3-->
<!--          .scaleLinear()-->
<!--          .domain(numericalDomain)-->
<!--          .range([padding, SvgWidth - padding]);-->
<!--        tickValues = xDomain.map((d) => Number(d.split("-")[0]));-->
<!--        tickValues.push(Number(xDomain[xDomain.length - 1].split("-")[1]));-->
<!--        bandwidth = (SvgWidth - 2 * padding) / xDomain.length;-->
<!--      } else {-->
<!--        // 类别型-->
<!--        xScale = d3-->
<!--          .scaleBand()-->
<!--          .domain(data.map(([category, value]) => category))-->
<!--          .range([padding, SvgWidth - padding])-->
<!--          .padding(0.1);-->
<!--        tickValues = xScale.domain();-->
<!--        bandwidth = xScale.bandwidth();-->
<!--      }-->
<!--      // y height scale-->
<!--      const yScale = d3-->
<!--        .scaleLinear()-->
<!--        .domain([0, yMax])-->
<!--        .range([SvgHeight - padding, padding]);-->

<!--      // 添加坐标轴-->
<!--      const xAxis = d3.axisBottom(xScale).tickValues(tickValues);-->
<!--      const yAxis = d3.axisLeft(yScale);-->

<!--      let colorScale = d3.scaleOrdinal(d3.schemeCategory10);-->
<!--      svg-->
<!--        .append("g")-->
<!--        .attr("transform", `translate(0, ${SvgHeight - padding})`)-->
<!--        .call(xAxis);-->

<!--      svg.append("g").attr("transform", `translate(${padding}, 0)`).call(yAxis);-->

<!--      // 添加 x 轴标题-->
<!--      svg-->
<!--        .append("text")-->
<!--        .attr("x", 700)-->
<!--        .attr("y", 370)-->
<!--        .attr("text-anchor", "middle")-->
<!--        .text(queryAttrs[0]);-->

<!--      // 添加 y 轴标题-->
<!--      svg-->
<!--        .append("text")-->
<!--        .attr("x", 70)-->
<!--        .attr("y", 40)-->
<!--        .attr("text-anchor", "middle")-->
<!--        .text(queryAttrs[1]);-->

<!--      // 绘制直方图-->
<!--      let container = svg-->
<!--        .selectAll(".container")-->
<!--        .data(data)-->
<!--        .enter()-->
<!--        .append("g")-->
<!--        .attr("class", "container");-->

<!--      // 非堆叠图-->
<!--      container-->
<!--        .filter((d) => typeof d[1] !== "object")-->
<!--        .append("rect")-->
<!--        .attr("x", ([category, value]) => {-->
<!--          if (isNumerical) {-->
<!--            let range = category.split("-").map((d) => Number(d));-->
<!--            return xScale(range[0]);-->
<!--          } else {-->
<!--            return xScale(category);-->
<!--          }-->
<!--        })-->
<!--        .attr("y", ([category, value]) => yScale(value))-->
<!--        .attr("width", bandwidth)-->
<!--        .attr(-->
<!--          "height",-->
<!--          ([category, value]) => SvgHeight - padding - yScale(value)-->
<!--        )-->
<!--        .attr("fill", "steelblue")-->
<!--        .attr("stroke", "#333")-->
<!--        .attr("stroke-with", "2px");-->

<!--      // 堆叠图-->
<!--      container-->
<!--        .filter((d) => typeof d[1] === "object")-->
<!--        .attr("transform", ([category, value]) => {-->
<!--          let xTrans;-->
<!--          if (isNumerical) {-->
<!--            let range = category.split("-").map((d) => Number(d));-->
<!--            xTrans = xScale(range[0]);-->
<!--          } else {-->
<!--            xTrans = xScale(category);-->
<!--          }-->
<!--          return `translate(${xTrans}, 0)`;-->
<!--        })-->
<!--        .selectAll("rect")-->
<!--        .data(-->
<!--          (d) => d[1],-->
<!--          (d) => d[0]-->
<!--        )-->
<!--        .join("rect")-->
<!--        .attr("class", ([category, value]) => `rect${category}`)-->
<!--        .attr("sumV", ([category, value], i, a) => {-->
<!--          if (i === 0) {-->
<!--            return value;-->
<!--          } else {-->
<!--            return +d3.select(a[i - 1]).attr("sumV") + value;-->
<!--          }-->
<!--        })-->
<!--        .attr("x", 0)-->
<!--        .attr("y", ([category, value], i, a) => {-->
<!--          let yPos;-->
<!--          if (i == 0) {-->
<!--            yPos = yScale(value);-->
<!--          } else {-->
<!--            yPos = yScale(d3.select(a[i]).attr("sumV"));-->
<!--          }-->
<!--          return yPos;-->
<!--        })-->
<!--        .attr("width", bandwidth)-->
<!--        .attr("height", ([category, value], i, a) => {-->
<!--          let yHeight;-->
<!--          if (i == 0) {-->
<!--            yHeight = SvgHeight - padding - yScale(value);-->
<!--          } else {-->
<!--            yHeight =-->
<!--              yScale(d3.select(a[i - 1]).attr("sumV")) - -->
<!--              yScale(d3.select(a[i]).attr("sumV"));-->
<!--          }-->
<!--          return yHeight;-->
<!--        })-->
<!--        .attr("fill", ([category, value]) =>-->
<!--          colorScale(secondCategory.indexOf(category))-->
<!--        );-->

<!--      if(isStack) {-->
<!--        // 添加 stack attr 标题-->
<!--        let legendG = svg.append('g').attr('transform', `translate(600, 40)`);-->
<!--        legendG.append("text")-->
<!--            .attr("x", 0)-->
<!--            .attr("y", 0)-->
<!--            .attr("text-anchor", "middle")-->
<!--            .text(queryAttrs[2]);-->
<!--        legendG.selectAll('rect')-->
<!--               .data(secondCategory)-->
<!--               .join('rect')-->
<!--               .attr('x', 0)-->
<!--               .attr('y', (d, i) => 20 + i * 30)-->
<!--               .attr('width', 20)-->
<!--               .attr('height', 20)-->
<!--               .attr("fill", (d, i) => colorScale(i));-->

<!--        legendG.selectAll('.tickText')-->
<!--            .data(secondCategory)-->
<!--            .join('text')-->
<!--            .attr('class', 'tickText')-->
<!--            .attr('x', 30)-->
<!--            .attr('y', (d, i) => 25 + i * 30)-->
<!--            .text(d => d)-->
<!--            .attr("stroke", '#555');-->
<!--      }-->
<!--    },-->

<!--    // 事件类函数-->
<!--    QueryConfirm() {-->
<!--      let QueryAttrs = this.DistributionAttr.map(d => {-->
<!--        return {-->
<!--          name: d-->
<!--        }-->
<!--      })-->
<!--      let QueryContent = this.QueryContent[0];-->
<!--      // 执行查询-->
<!--      let [queryRes, axisAttr] = this.executeQuery(QueryAttrs, QueryContent);-->
<!--      // 绘制查询结果-->
<!--      this.drawQueryResult(queryRes, axisAttr);-->
<!--    },-->
<!--    onDragEnd() {-->

<!--    },-->

<!--    // 细节类函数-->
<!--    // 范围取整函数-->
<!--    roundedScope(dataMin, dataMax) {-->
<!--      return [Math.floor(dataMin), Math.ceil(dataMax)];-->
<!--    },-->
<!--    // input: d: object-->
<!--    // 目前采用的是 d3.autoType 识别的效果-->
<!--    // 相对来说不会那么准确，后续如果需要优化，则可以用手动识别的方式-->
<!--    getAttrType(d) {-->
<!--      let AttrTypeMap = Object.keys(d).reduce((ret, attribute) => {-->
<!--        const type = typeof d[attribute];-->
<!--        ret[attribute] =-->
<!--          type === "number" ? "#" : type === "string" ? "A" : "T";-->
<!--        return ret;-->
<!--      }, {});-->
<!--      return AttrTypeMap;-->
<!--    },-->
<!--    // 直方图数据生成器-->
<!--    histogramDataGenerator(data, value, domain = undefined) {-->
<!--      if (domain === undefined) {-->
<!--        domain = this.roundedScope(...this.AttrRangeMap[value]);-->
<!--      }-->
<!--      let histogramDataGenerator = d3-->
<!--        .histogram()-->
<!--        .value(function (d) {-->
<!--          return d[value];-->
<!--        })-->
<!--        .domain(domain) // 指定数据的范围-->
<!--        .thresholds(-->
<!--          d3.range(domain[0], domain[1], (domain[1] - domain[0]) / 10)-->
<!--        );-->

<!--      return histogramDataGenerator(data);-->
<!--    },-->
<!--    // 封装 getHQueryRes 和 getCQueryRes-->
<!--    getQueryRes(QueryAttrName, QueryContent, data, dataDomain) {-->
<!--      if (this.AttrTypeMap[QueryAttrName] === "#") {-->
<!--        let bins = this.histogramDataGenerator(data, QueryAttrName, dataDomain);-->
<!--        let queryRes = this.getHQueryRes(bins, QueryContent); // histogram query-->
<!--        return [bins, queryRes];-->
<!--      } else if (this.AttrTypeMap[QueryAttrName] === "A") {-->
<!--        let groupedData = d3.group(data, (d) => d[QueryAttrName]);-->
<!--        let bins = Array.from(groupedData);-->
<!--        let queryRes = this.getCQueryRes(bins, QueryContent); // categorical query-->
<!--        bins = bins.map((bin) => bin[1]);-->
<!--        return [bins, queryRes];-->
<!--      }-->
<!--    },-->
<!--    // get histogram query result-->
<!--    getHQueryRes(bins, QueryContent) {-->
<!--      let binsData = bins.map((bin) => {-->
<!--        // 多分布-->
<!--        if (Array.isArray(bin[0])) {-->
<!--          return [];-->
<!--        } else {-->
<!--          if (QueryContent === "#COUNT") {-->
<!--            return bin.length;-->
<!--          } else {-->
<!--            return d3.sum(bin, (d) => d[QueryContent]);-->
<!--          }-->
<!--        }-->
<!--      });-->
<!--      let binsMap = bins.reduce((pre, cur, i) => {-->
<!--        pre[`${cur.x0}-${cur.x1}`] = binsData[i];-->
<!--        return pre;-->
<!--      }, {});-->
<!--      return binsMap;-->
<!--    },-->
<!--    // get categorical query result-->
<!--    getCQueryRes(bins, QueryContent) {-->
<!--      let binsData = bins.map((bin) => {-->
<!--        // 多分布-->
<!--        if (Array.isArray(bin[1][0])) {-->
<!--          return [];-->
<!--        } else {-->
<!--          if (QueryContent === "#COUNT") {-->
<!--            return bin[1].length;-->
<!--          } else {-->
<!--            return d3.sum(bin[1], (d) => d[QueryContent]);-->
<!--          }-->
<!--        }-->
<!--      });-->
<!--      let binsMap = bins.reduce((pre, cur, i) => {-->
<!--        pre[`${cur[0]}`] = binsData[i];-->
<!--        return pre;-->
<!--      }, {});-->
<!--      return binsMap;-->
<!--    },-->
<!--  },-->

<!--  created() {-->
<!--    // 读数据-->
<!--    d3.csv("./data/cost_of_living_us.csv", d3.autoType).then((dataset) => {-->
<!--      this.Dataset = dataset;-->
<!--      this.DatasetColumns = dataset.columns;-->
<!--      this.AttrTypeMap = this.getAttrType(dataset[0]);-->
<!--    });-->

<!--    d3.csv("./data/attr_range.csv", d3.autoType).then((data) => {-->
<!--      this.AttrRangeMap = data.reduce((pre, cur) => {-->
<!--        pre[cur["attribute"]] = [cur["min"], cur["max"]];-->
<!--        return pre;-->
<!--      }, {});-->
<!--    });-->
<!--  },-->
<!--  mounted() {},-->
<!--};-->
<!--</script>-->

<!--<style scoped>-->
<!--/* base style start */-->
<!--.ColorBox {-->
<!--  background-color: #fff;-->
<!--}-->

<!--.FlexRow {-->
<!--  display: flex;-->
<!--  flex-direction: row;-->
<!--}-->

<!--.MainHeading {-->
<!--  font-size: 20px;-->
<!--  margin: 5px 0 5px 5px;-->
<!--}-->

<!--.SubHeading {-->
<!--  font-size: 18px;-->
<!--  margin: 5px 0 5px 5px;-->
<!--}-->
<!--/* base style end */-->

<!--/* base frame start */-->
<!--.LeftPart,-->
<!--.MidPart,-->
<!--.RightPart {-->
<!--  margin: 10px;-->
<!--  height: calc(100% - 20px);-->
<!--}-->
<!--.LeftPart {-->
<!--  width: 25%;-->
<!--  margin-right: 5px;-->
<!--}-->

<!--.MidPart {-->
<!--  width: 50%;-->
<!--  margin-left: 5px;-->
<!--  margin-right: 5px;-->

<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--}-->

<!--.RightPart {-->
<!--  margin-left: 5px;-->
<!--  width: 25%;-->
<!--}-->
<!--/* base frame end */-->

<!--/* LeftPart style start */-->
<!--.QueryInputBody {-->
<!--  height: calc(100% - 25px);-->
<!--}-->

<!--.QueryInputPart {-->
<!--  height: 100%;-->
<!--  flex: 1;-->
<!--}-->

<!--.QueryTaskInputPart {-->
<!--  height: calc(20%);-->
<!--}-->

<!--.QueryTaskInput {-->
<!--  height: 40px;-->
<!--}-->

<!--.QueryInput {-->
<!--  margin: 10px 0;-->
<!--  height: calc(50% - 20px);-->
<!--}-->

<!--.NABody {-->
<!--  overflow-y: auto;-->
<!--  height: calc(100% - 27px);-->
<!--}-->

<!--.QueryListShow {-->
<!--  height: 30%;-->
<!--}-->

<!--.CurGraph {-->
<!--  width: 800px;-->
<!--  height: 400px;-->
<!--}-->
<!--/* LeftPart style end */-->

<!--/* MidPart style start */-->
<!--.QueryPreview,-->
<!--.CurGraphShowPart {-->
<!--  width: 100%;-->
<!--}-->
<!--.QueryPreview {-->
<!--  height: 40%;-->
<!--}-->
<!--.CurGraphShowPart {-->
<!--  margin-top: 10px;-->
<!--  height: calc(60% - 10px);-->
<!--}-->

<!--.CurQueryAttrListPart, .DistributionAttrPart, .QueryContentPart{-->
<!--  min-height: 50px;-->
<!--}-->
<!--/* MidPart style end */-->

<!--/* RightPart style start */-->
<!--.HistoryGraphPart {-->
<!--  height: 100%;-->
<!--}-->
<!--/* RightPart style end */-->
<!--</style>-->

<template>
    <div>
        <vue-slider v-model="sliderValues" :min="0" :max="100" :multiple="true"></vue-slider>
        <button @click="moveFirstSlider">移动第一个滑块</button>
        <button @click="moveSecondSlider">移动第二个滑块</button>
        <p>当前值: {{ sliderValues }}</p>
    </div>
</template>

<script>
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";


export default {
    components: { VueSlider },
    data() {
        return {
            sliderValues: [25, 75]  // 初始值，假设是两个滑块的滑动条
        };
    },
    methods: {
        moveFirstSlider() {
            // 修改第一个滑块的值
            this.sliderValues[0] += 10;
            if (this.sliderValues[0] > this.sliderValues[1]) {
                // 确保第一个滑块的值不超过第二个滑块的值
                this.sliderValues[0] = this.sliderValues[1] - 1;
            }
            if (this.sliderValues[0] > 100) {
                // 确保值不超过最大值
                this.sliderValues[0] = 100;
            }
        },
        moveSecondSlider() {
            // 修改第二个滑块的值
            this.sliderValues[1] -= 10;
            if (this.sliderValues[1] < this.sliderValues[0]) {
                // 确保第二个滑块的值不小于第一个滑块的值
                this.sliderValues[1] = this.sliderValues[0] + 1;
            }
            if (this.sliderValues[1] < 0) {
                // 确保值不小于最小值
                this.sliderValues[1] = 0;
            }
        }
    }
};
</script>