<template>
  <vue-slider
      style="width: 200px; height: 20px"
      v-model="value"></vue-slider>

  <div class="attrList"></div>
  <!-- 属性列表 -->
  <div class="Fields">
    <el-button
      class="attrBar"
      :type="chosenAttrs.includes(attr) ? 'primary' : 'default'"
      @click="chooseCurAttr(attr)"
      v-for="attr in attrs"
      :key="attr"
    >
      {{ attr + " (" + attrTypeMap[attr] + ")" }}
    </el-button>
  </div>
  <div class="testBtn">
    <!-- 数值型 + #COUNT -->
    <button @click="execQuery1" title="food_cost(#)  &  #COUNT(#)">
      Query 1
    </button>
    <!-- 类别型 + #COUNT -->
    <button @click="execQuery2" title="family_member_count(A)  &  #COUNT(#)">
      Query 2
    </button>
    <!-- 数值型 + 数值型（sum） -->
    <button @click="execQuery3" title="food_cost(#)  &  housing_cost(sum)">
      Query 3
    </button>

    <!-- 类别型 + 数值型（sum） -->
    <button
      @click="execQuery4"
      title="family_member_count(A)  &  housing_cost(sum)"
    >
      Query 4
    </button>

    <!-- 数值型 + 数值型 + #COUNT -->
    <button
      @click="execQuery5"
      title="food_cost(#)  & housing_cost(#) &  #COUNT"
    >
      Query 5
    </button>

    <!-- 数值型 + 类别型 + #COUNT -->
    <button
      @click="execQuery6"
      title="food_cost(#)  & family_member_count(A) &  #COUNT"
    >
      Query 6
    </button>

    <!-- 类别型 + 类别型 + #COUNT -->
    <button
      @click="execQuery7"
      title="isMetro(A)  & family_member_count(A) &  #COUNT"
    >
      Query 7
    </button>

    <!-- 数值型 + 数值型 + 数值型（sum） -->
    <button
      @click="execQuery8"
      title="food_cost(#) & housing_cost(#) & #healthcare_cost(sum)"
    >
      Query 8
    </button>

    <!-- 数值型 + 类别型 + 数值型（sum） -->
    <button
      @click="execQuery9"
      title="food_cost(#) & family_member_count(A) & #healthcare_cost(sum)"
    >
      Query 9
    </button>

    <!-- 类别型 + 类别型 + 数值型（sum） -->
    <button
      @click="execQuery10"
      title="isMetro(A)  & family_member_count(A) &  #healthcare_cost(sum)"
    >
      Query 10
    </button>
  </div>
  <svg class="QueryResultSvg"></svg>


</template>

<script>
import axios from "axios";
import * as d3 from "d3";
import VueSlider from 'vue-slider-component';
import 'vue-slider-component/theme/default.css';

export default {
  name: "Test",
  components: {VueSlider},
  data() {
    return {
      rawData: [],
      attrs: [],
      attrTypeMap: [], // A: categorical  #: numerical  T: temporal

      chosenAttrs: [],

      svgWidth: 800,
      svgHeight: 500,
      bins: 10,

      AttrRangeMap: {},

      value: [0, 20, 60],
    };
  },
  computed: {
    QueryTemplate(chosenAttrs) {
      return {
        x: {
          attrName: "aaa",
        },
        y: {
          attrName: "aaa",
        },
      };
    },
  },
  methods: {
    // 范围取整函数
    roundedScope(dataMin, dataMax) {
      return [Math.floor(dataMin), Math.ceil(dataMax)];
    },

    // 直方图数据生成器
    histogramDataGenerator(data, value, domain = undefined) {
      if (domain === undefined) {
        domain = this.roundedScope(...this.AttrRangeMap[value]);
      }
      let histogramDataGenerator = d3
        .histogram()
        .value(function (d) {
          return d[value];
        })
        .domain(domain) // 指定数据的范围
        .thresholds(
          d3.range(domain[0], domain[1], (domain[1] - domain[0]) / 10)
        );

      return histogramDataGenerator(data);
    },

    // input: d: object
    // 目前采用的是 d3.autoType 识别的效果
    // 相对来说不会那么准确，后续如果需要优化，则可以用手动识别的方式
    getAttrType(d) {
      let attrTypeMap = Object.keys(d).reduce((ret, attribute) => {
        const type = typeof d[attribute];
        ret[attribute] =
          type === "number" ? "#" : type === "string" ? "A" : "T";
        return ret;
      }, {});
      return attrTypeMap;
    },
    // 执行查询
    executeQuery(QueryAttrs, QueryContent) {
      // 单属性 + COUNT 的情况
      if (QueryAttrs.length === 1) {
        let QueryAttrName = QueryAttrs[0].name;
        let queryRes = this.getQueryRes(
          QueryAttrName,
          QueryContent,
          this.rawData
        );
        let axisAttr = [QueryAttrName, QueryContent];
        return [queryRes[1], axisAttr];
      }
      // 双属性查询的情况
      else {
        let QueryAttrNames = [QueryAttrs[0].name, QueryAttrs[1].name];
        let [bins, queryRes] = this.getQueryRes(
          QueryAttrNames[0],
          QueryContent,
          this.rawData
        );
        let axisAttr = [QueryAttrNames[0], QueryContent, QueryAttrNames[1]];
        let binKeys = Object.keys(queryRes);
        let secondDataDomain;
        if (this.attrTypeMap[QueryAttrNames[1]] === "#") {
          secondDataDomain = [
            d3.min(bins, (bin) => d3.min(bin, (d) => d[QueryAttrNames[1]])),
            d3.max(bins, (bin) => d3.max(bin, (d) => d[QueryAttrNames[1]])),
          ];
        }

        for (let idx in bins) {
          let [, secondaQueryRes] = this.getQueryRes(
            QueryAttrNames[1],
            QueryContent,
            bins[idx],
            secondDataDomain
          );
          queryRes[binKeys[idx]] = secondaQueryRes;
        }
        return [queryRes, axisAttr];
      }
    },
    // 封装 getHQueryRes 和 getCQueryRes
    getQueryRes(QueryAttrName, QueryContent, data, dataDomain) {
      if (this.attrTypeMap[QueryAttrName] === "#") {
        let bins = this.histogramDataGenerator(data, QueryAttrName, dataDomain);
        let queryRes = this.getHQueryRes(bins, QueryContent); // histogram query
        return [bins, queryRes];
      } else if (this.attrTypeMap[QueryAttrName] === "A") {
        let groupedData = d3.group(data, (d) => d[QueryAttrName]);
        let bins = Array.from(groupedData);
        let queryRes = this.getCQueryRes(bins, QueryContent); // categorical query
        bins = bins.map((bin) => bin[1]);
        return [bins, queryRes];
      }
    },
    // get histogram query result
    getHQueryRes(bins, QueryContent) {
      let binsData = bins.map((bin) => {
        // 多分布
        if (Array.isArray(bin[0])) {
          return [];
        } else {
          if (QueryContent === "#COUNT") {
            return bin.length;
          } else {
            return d3.sum(bin, (d) => d[QueryContent]);
          }
        }
      });
      let binsMap = bins.reduce((pre, cur, i) => {
        pre[`${cur.x0}-${cur.x1}`] = binsData[i];
        return pre;
      }, {});
      return binsMap;
    },
    // get categorical query result
    getCQueryRes(bins, QueryContent) {
      let binsData = bins.map((bin) => {
        // 多分布
        if (Array.isArray(bin[1][0])) {
          return [];
        } else {
          if (QueryContent === "#COUNT") {
            return bin[1].length;
          } else {
            return d3.sum(bin[1], (d) => d[QueryContent]);
          }
        }
      });
      let binsMap = bins.reduce((pre, cur, i) => {
        pre[`${cur[0]}`] = binsData[i];
        return pre;
      }, {});
      return binsMap;
    },

    // 绘制查询结果
    drawQueryResult(queryRes, queryAttrs) {
      let [svgWidth, svgHeight] = [this.svgWidth, this.svgHeight];
      let padding = 70;
      let yMax;

      // 创建 SVG 元素
      const svg = d3.select(".QueryResultSvg");
      svg.selectAll("*").remove();

      // 将 Map 数据转换为数组
      const data = Object.entries(queryRes);
      let secondCategory;
      if (typeof data[0][1] === "object") {
        secondCategory = Object.keys(data[0][1]);
        for (let d of data) {
          d[1] = Object.entries(d[1]);
        }
        yMax = d3.max(data, ([category, value]) =>
          d3.sum(value, ([c, v]) => v)
        );
      } else {
        yMax = d3.max(data, ([category, value]) => value);
      }

      // 设置比例尺
      let xDomain = data.map(([category, value]) => category);
      let xScale;
      let bandwidth;
      let isNumerical = !isNaN(xDomain[0].split("-")[0]);
      let tickValues = [];
      if (isNumerical) {
        // 数值型
        let numericalDomain = [
          Number(xDomain[0].split("-")[0]),
          Number(xDomain[xDomain.length - 1].split("-")[1]),
        ];
        xScale = d3
          .scaleLinear()
          .domain(numericalDomain)
          .range([padding, svgWidth - padding]);
        tickValues = xDomain.map((d) => Number(d.split("-")[0]));
        tickValues.push(Number(xDomain[xDomain.length - 1].split("-")[1]));
        bandwidth = (svgWidth - 2 * padding) / xDomain.length;
      } else {
        // 类别型
        xScale = d3
          .scaleBand()
          .domain(data.map(([category, value]) => category))
          .range([padding, svgWidth - padding])
          .padding(0.1);
        tickValues = xScale.domain();
        bandwidth = xScale.bandwidth();
      }
      // y height scale
      const yScale = d3
        .scaleLinear()
        .domain([0, yMax])
        .range([svgHeight - padding, padding]);

      // 添加坐标轴
      const xAxis = d3.axisBottom(xScale).tickValues(tickValues);
      const yAxis = d3.axisLeft(yScale);

      let colorScale = d3.scaleOrdinal(d3.schemeCategory10);
      svg
        .append("g")
        .attr("transform", `translate(0, ${svgHeight - padding})`)
        .call(xAxis);

      svg.append("g").attr("transform", `translate(${padding}, 0)`).call(yAxis);

      // 添加轴标题
      svg
        .append("text")
        .attr("x", 700)
        .attr("y", 470)
        .attr("text-anchor", "middle")
        .text(queryAttrs[0]);

      // 添加 y 轴标题
      svg
        .append("text")
        .attr("x", 70)
        .attr("y", 40)
        .attr("text-anchor", "middle")
        .text(queryAttrs[1]);

      // 绘制直方图
      let container = svg
        .selectAll(".container")
        .data(data)
        .enter()
        .append("g")
        .attr("class", "container");

      // 非堆叠图
      container
        .filter((d) => typeof d[1] !== "object")
        .append("rect")
        .attr("x", ([category, value]) => {
          if (isNumerical) {
            let range = category.split("-").map((d) => Number(d));
            return xScale(range[0]);
          } else {
            return xScale(category);
          }
        })
        .attr("y", ([category, value]) => yScale(value))
        .attr("width", bandwidth)
        .attr(
          "height",
          ([category, value]) => svgHeight - padding - yScale(value)
        )
        .attr("fill", "steelblue")
        .attr("stroke", "#333")
        .attr("stroke-with", "2px");

      // 堆叠图
      container
        .filter((d) => typeof d[1] === "object")
        .attr("transform", ([category, value]) => {
          let xTrans;
          if (isNumerical) {
            let range = category.split("-").map((d) => Number(d));
            xTrans = xScale(range[0]);
          } else {
            xTrans = xScale(category);
          }
          return `translate(${xTrans}, 0)`;
        })
        .selectAll("rect")
        .data(
          (d) => d[1],
          (d) => d[0]
        )
        .join("rect")
        .attr("class", ([category, value]) => `rect${category}`)
        .attr("sumV", ([category, value], i, a) => {
          if (i === 0) {
            return value;
          } else {
            return +d3.select(a[i - 1]).attr("sumV") + value;
          }
        })
        .attr("x", 0)
        .attr("y", ([category, value], i, a) => {
          let yPos;
          if (i == 0) {
            yPos = yScale(value);
          } else {
            yPos = yScale(d3.select(a[i]).attr("sumV"));
          }
          return yPos;
        })
        .attr("width", bandwidth)
        .attr("height", ([category, value], i, a) => {
          let yHeight;
          if (i == 0) {
            yHeight = svgHeight - padding - yScale(value);
          } else {
            yHeight =
              yScale(d3.select(a[i - 1]).attr("sumV")) -
              yScale(d3.select(a[i]).attr("sumV"));
          }
          return yHeight;
        })
        .attr("fill", ([category, value]) =>
          colorScale(secondCategory.indexOf(category))
        );
    },

    chooseCurAttr(attr) {
      if (this.chosenAttrs.includes(attr)) {
        this.chosenAttrs.splice(this.chosenAttrs.indexOf(attr), 1);
      } else {
        if (this.chosenAttrs.length == 2) {
          return;
        }
        this.chosenAttrs.push(attr);
      }
    },

    // test function
    execQuery1() {
      this.value = [0, 50, 100];
      let QueryAttrs = [
        {
          name: "food_cost",
        },
      ];
      let QueryContent = "#COUNT";
      // 执行查询
      let [queryRes, axisAttr] = this.executeQuery(QueryAttrs, QueryContent);
      // 绘制查询结果
      this.drawQueryResult(queryRes, axisAttr);
    },
    execQuery2() {
      let QueryAttrs = [
        {
          name: "family_member_count",
        },
      ];
      let QueryContent = "#COUNT";
      // 执行查询
      let [queryRes, axisAttr] = this.executeQuery(QueryAttrs, QueryContent);
      // 绘制查询结果
      this.drawQueryResult(queryRes, axisAttr);
    },
    execQuery3() {
      let QueryAttrs = [
        {
          name: "food_cost",
        },
      ];
      let QueryContent = "housing_cost";
      // 执行查询
      let [queryRes, axisAttr] = this.executeQuery(QueryAttrs, QueryContent);
      // 绘制查询结果
      this.drawQueryResult(queryRes, axisAttr);
    },
    execQuery4() {
      let QueryAttrs = [
        {
          name: "family_member_count",
        },
      ];
      let QueryContent = "housing_cost";
      // 执行查询
      let [queryRes, axisAttr] = this.executeQuery(QueryAttrs, QueryContent);
      // 绘制查询结果
      this.drawQueryResult(queryRes, axisAttr);
    },
    execQuery5() {
      let QueryAttrs = [
        {
          name: "food_cost",
        },
        {
          name: "housing_cost",
        },
      ];
      let QueryContent = "#COUNT";
      // 执行查询
      let [queryRes, axisAttr] = this.executeQuery(QueryAttrs, QueryContent);
      // 绘制查询结果
      this.drawQueryResult(queryRes, axisAttr);
    },
    execQuery6() {
      let QueryAttrs = [
        {
          name: "food_cost",
        },
        {
          name: "family_member_count",
        },
      ];
      let QueryContent = "#COUNT";
      // 执行查询
      let [queryRes, axisAttr] = this.executeQuery(QueryAttrs, QueryContent);
      // 绘制查询结果
      this.drawQueryResult(queryRes, axisAttr);
    },
    execQuery7() {
      let QueryAttrs = [
        {
          name: "isMetro",
        },
        {
          name: "family_member_count",
        },
      ];
      let QueryContent = "#COUNT";
      // 执行查询
      let [queryRes, axisAttr] = this.executeQuery(QueryAttrs, QueryContent);
      // 绘制查询结果
      this.drawQueryResult(queryRes, axisAttr);
    },
    execQuery8() {
      let QueryAttrs = [
        {
          name: "food_cost",
        },
        {
          name: "housing_cost",
        },
      ];
      let QueryContent = "healthcare_cost";
      // 执行查询
      let [queryRes, axisAttr] = this.executeQuery(QueryAttrs, QueryContent);
      // 绘制查询结果
      this.drawQueryResult(queryRes, axisAttr);
    },
    execQuery9() {
      let QueryAttrs = [
        {
          name: "food_cost",
        },
        {
          name: "family_member_count",
        },
      ];
      let QueryContent = "healthcare_cost";
      // 执行查询
      let [queryRes, axisAttr] = this.executeQuery(QueryAttrs, QueryContent);
      // 绘制查询结果
      this.drawQueryResult(queryRes, axisAttr);
    },
    execQuery10() {
      let QueryAttrs = [
        {
          name: "isMetro",
        },
        {
          name: "family_member_count",
        },
      ];
      let QueryContent = "healthcare_cost";
      // 执行查询
      let [queryRes, axisAttr] = this.executeQuery(QueryAttrs, QueryContent);
      // 绘制查询结果
      this.drawQueryResult(queryRes, axisAttr);
    },
  },
  watch: {},
  created() {},
  mounted() {
    this.value = [0, 30, 40, 100];

    // 读数据
    d3.csv("./data/cost_of_living_us.csv", d3.autoType).then((data) => {
      this.rawData = data;
      let attrs = (this.attrs = data.columns);
      let attrTypeMap = (this.attrTypeMap = this.getAttrType(data[0]));
      console.log(attrTypeMap);
      let rankMap = { A: 2, T: 1, "#": 0 };
      this.attrs = this.attrs.sort(
        (a, b) => rankMap[attrTypeMap[b]] - rankMap[attrTypeMap[a]]
      );
    });

    d3.csv("./data/attr_range.csv", d3.autoType).then((data) => {
      this.AttrRangeMap = data.reduce((pre, cur) => {
        pre[cur["attribute"]] = [cur["min"], cur["max"]];
        return pre;
      }, {});
    });


  },
};
</script>

<style scoped>
.Fields {
  display: flex;
  flex-direction: column;
}
.attrBar {
  margin: 10px 0;
}

.QueryResultSvg {
  width: 800px;
  height: 500px;
}

.testBtn {
  display: flex;
}
.testBtn button {
  height: 20px;
  margin: 10px;
}
</style>
