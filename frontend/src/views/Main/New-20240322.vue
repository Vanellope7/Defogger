<template>
  <!-- 界面左部分视图 -->
    <div class="LeftPart">
        <!-- 数据库选择与信息展示 -->
        <div class="BaseMessPart ColorBox">
            <!-- <div class="MainHeading">Exploration Entrance</div> -->
            <div class="FlexRow" style="margin-top: 5px">
                <span style="margin-left: 5px">Database: </span>
                <el-select
                        v-model="CurDatabase"
                        class="m-2"
                        placeholder="Select"
                        style="width: 180px; margin-left: 5px"
                        @change="resetDatabase"
                >
                    <el-option
                            v-for="item in DataBaseList"
                            :key="item"
                            :label="item"
                            :value="item"
                    />
                </el-select>
                <div class="MainText" style="margin-left: auto; margin-right: 10px">
                    Privacy budget (&epsilon;) used:
                    {{
                    (
                        BaseEpsilonMap[CurDatabase] - TotalEpsilonMap[CurDatabase]
                    ).toFixed(2)
                    }}
                    out of
                    {{ BaseEpsilonMap[CurDatabase] }}
                </div>
            </div>
        </div>

        <!-- 查询输入 -->
        <div class="QueryInputPart ColorBox">
            <div class="MainHeading">Information Reservation</div>
            <el-divider border-style="dashed" class="TextDivider" />
            <div class="SubHeading">Attributes in the database</div>
            <svg class="DBAttrBody">
                <g class="LineContainer"></g>

                <g class="AttrSetContainer" transform="translate(15, 30)">
                    <g transform="translate(340, -20)">
                        <rect
                                x="0"
                                y="0"
                                width="20"
                                height="20"
                                :fill="BaseColorMap['red-sensitive']"
                        ></rect>
                        <text x="25" y="14" class="legendMText">Sensitive</text>
                    </g>
                    <g transform="translate(460, -20)">
                        <rect
                                x="0"
                                y="0"
                                width="20"
                                height="20"
                                :fill="BaseColorMap['blue-normal']"
                        >
                        </rect>
                        <text x="25" y="14" class="legendMText">Public</text>
                    </g>
                    <g
                            class="DBAttrItemBg"
                            :id="`DBAttrItemBg${i}`"
                            v-for="(column, i) in DatasetColumns"
                            :key="column"
                            :name="column"
                    >
                        <rect
                                :x="0"
                                :y="0"
                                rx="5"
                                ry="5"
                                :id="`AttrRectBg${i}`"
                                width="170"
                                height="28"
                                :fill="BaseColorMap['grey-normal']"
                        >

                        </rect>
                        <text
                                x="0"
                                :y="15"
                                :id="`AttrTextBg${i}`"
                                dominant-baseline="middle"
                                text-anchor="middle"
                                :fill="BaseColorMap['white']"
                        >
                            {{ column }}
                        </text>
                    </g>
                    <g
                            class="DBAttrItem"
                            v-for="(column, i) in DatasetColumns"
                            :key="column"
                            :name="column"
                            @dblclick="dblclickDataColumn(column)"
                    >
                        <title>{{AttrMessMap[column]}}</title>
                        <g v-show="AttrIntentMap[column] === undefined">
                            <rect
                                    :x="0"
                                    :y="0"
                                    rx="5"
                                    ry="5"
                                    :class="{
                  AttrRect: true,
                  SingleAttrQuery: ColumnDbClickMap[column],
                }"
                                    width="170"
                                    height="28"
                                    :fill="
                  AttrSensitive[column]
                    ? BaseColorMap['red-sensitive']
                    : BaseColorMap['blue-normal']
                "
                            ></rect>
                            <text
                                    x="0"
                                    :y="15"
                                    class="AttrText"
                                    dominant-baseline="middle"
                                    text-anchor="middle"
                                    :fill="BaseColorMap['white']"
                            >
                                {{ column }}
                            </text>
                        </g>
                        <g
                                class="intentNode"
                                :id="`intentNode${column}`"
                                v-show="AttrIntentMap[column]"
                        >
                            <circle
                                    cx="5"
                                    cy="14"
                                    r="30"
                                    :stroke="
                                    AttrSensitive[column]
                    ? BaseColorMap['red-sensitive']
                    : BaseColorMap['blue-normal']
                "
                                    stroke-width="3px"
                                    :fill="BaseColorMap['white']"
                            ></circle>
                            <text x="70" y="20">{{ column }}</text>
                        </g>
                    </g>
                </g>
                <!--                // query input-->
                <text x="5" y="230" style="font-size: 18px; fill: #666">
                    Exploration Intent
                </text>
                <g class="QueryContainer" transform="translate(15, 250)">
                    <rect
                            x="0"
                            y="0"
                            width="calc(100% - 30px)"
                            height="40%"
                            fill="none"
                            :stroke="BaseColorMap['grey-normal']"
                            stroke-dasharray="3 2"
                    ></rect>
                </g>
                <rect
                    x="15"
                    y="510"
                    width="120"
                    height="130"
                    fill="none"
                    stroke-width="1px"
                    stroke-dasharray="3 2"
                    :stroke="BaseColorMap['grey-normal']"
                ></rect>
                <g class="queryInputLegend" transform="translate(0, 550)">


                    <g transform="translate(0, -20)">
                        <text x="30" y="0" class="legendMText">
                            Distribution:
                        </text>
                        <line
                            x1="25"
                            x2="120"
                            y1="5"
                            y2="5"
                            stroke-width="1px"
                            stroke-dasharray="3 2"
                            :stroke="BaseColorMap['grey-normal']"
                        ></line>
                        <path
                                d="M30.509,11.34L35.364,19.274L40.218,14.672L45.072,10.04L49.927,19.542L54.781,10L59.635,15.784L64.49,12.107L69.344,18.464L74.199,18.645"
                                :stroke="BaseColorMap['grey-normal']"
                                stroke-width="2"
                                fill="none"
                        ></path>
                        <text x="30" y="35" class="legendMText">
                            Verified
                        </text>
                        <text x="30" y="50" class="legendMText">
                            (width-95% CI)
                        </text>
                    </g>
                    <g transform="translate(0, 40)">
                        <path
                                d="M30.509,11.34L35.364,19.274L40.218,14.672L45.072,10.04L49.927,19.542L54.781,10L59.635,15.784L64.49,12.107L69.344,18.464L74.199,18.645"
                                :stroke="BaseColorMap['grey-light']"
                                stroke-width="2"
                                fill="none"
                        ></path>
                        <text x="30" y="35" class="legendMText">Simulated</text>
                    </g>
                </g>
                <g transform="translate(0, 110)">
                    <text x="5" y="560" style="font-size: 18px; fill: #666">
                        Simulated Distribution
                    </text>
                    <g class="CurAttrHistogram" transform="translate(15, 580)">
                        <rect
                                x="0"
                                y="0"
                                width="calc(100% - 30px)"
                                height="27%"
                                fill="none"
                                :stroke="BaseColorMap['grey-normal']"
                                stroke-dasharray="3 2"
                        ></rect>
                    </g>
                </g>
            </svg>
            <div class="ExplorationProgress FlexRow">
              <div>Progress of exploration:</div>
              <vue-slider  class="ExplorationProgressSlider" :width="80" :marks="ExplorationProgressMarks"
                           @change="handleEPSliderChange"
                          v-model="ExplorationProgressVal"></vue-slider>
            </div>
            <div class="ResetButton">
                <el-button
                        @click="ResetHistogram"
                        type="primary"
                        v-if="AttrSensitive[CurThisNodeName]"
                >Reset</el-button
                >
            </div>

            <!-- 输入框和确认按钮 -->
            <div class="CorrInputGroup FlexRow" v-show="ShowCorrInput">
                <span>{{ CurLineName.replace("±", " and ") + ": " }}</span>
                <el-input
                        v-model="CurInputText"
                        @keydown.enter="confirmText"
                        style="width: 50px; margin-left: 10px"
                ></el-input>
            </div>
        </div>

        <!-- 查询历史 -->
        <!-- <div class="QueryHistoryPart ColorBox">
      <div class="MainHeading">Query History</div>
      <el-table :data="QueryHistory" stripe style="width: 100%">
        <el-table-column prop="queryAttr" label="Query attr" width="180" />
        <el-table-column prop="epsilon" label="Private budget" width="180" />
        <el-table-column prop="graph" label="Query result" />
      </el-table>
    </div> -->
    </div>

    <div class="MidPart">
        <div class="QueryTemplatePart ColorBox">
            <div class="QueryTemplateTop">
                <div class="MainHeading">Data Request Panel</div>
                <el-divider border-style="dashed" class="TextDivider" />
                <!-- <div>Vis Type:</div>
      <el-select
        v-model="CurVisType"
        class="m-2"
        placeholder="Select"
        style="width: 200px"
      >
        <el-option
          v-for="item in CurVisTypeList"
          :key="item"
          :label="item"
          :value="item"
        />
      </el-select> -->

                <!-- <div>Query Content:</div>
      <el-select
        v-model="CurQueryContent"
        class="m-2"
        placeholder="Select"
        style="width: 200px"
      >
        <el-option
          v-for="item in QueryContentOption"
          :key="item"
          :label="item"
          :value="item"
        />
      </el-select> -->
                <!-- <div>Query Content:</div> -->
                <!-- <div>展示已选查询的数值型属性查询粒度</div>
      <el-button type="primary" @click="ConfirmQueryTemplate"
        >confirm query template</el-button
      > -->
                <div class="SubHeading">Set division:</div>
                <div
                        class="QueryGranularityAdjust FlexRow"
                        v-for="(cna, cnaIdx) in CurExeQuery"
                        :key="cna"
                >
                    <el-button
                            @click="deleteExeAttr(cna)"
                            size="small"
                            style="width: 20px; height: 20px"
                    >
                        <el-icon style="width: 20px; height: 20px; font-size: 18px"
                        ><Close
                        /></el-icon>
                    </el-button>
                    <div>{{ cna }}</div>

                    <div>:</div>
                    <!-- 数值型 -->
                    <svg class="tickSvg">
                        <line
                                x1="0"
                                x2="200"
                                y1="30"
                                y2="30"
                                stroke-width="4px"
                                :stroke="BaseColorMap['blue-normal']"
                        ></line>
                        <g v-if="AttrTypeMap[cna] === '#'">
                            <g
                                    :key="i + 1"
                                    v-for="(bin, i) in AttrBinRangeMap[cna]"
                                    :transform="`translate(${
                  (190 / (AttrBinRangeMap[cna].length - 1)) * (i) + 5
                }, 25)`"
                            >
                                <polygon
                                        v-if="i!==0 && i!== AttrBinRangeMap[cna].length-1"
                                        points="-8,0 8,0 0,13"
                                        transform="translate(0, -10)"
                                        @click="reverseQueryBin(cna, bin)"
                                        :stroke="BaseColorMap['grey-normal']"
                                        :fill="
                                        AttrQueryBinRangeMap[cna].includes(bin)
                                          ? BaseColorMap['grey-normal']
                                          : BaseColorMap['white']
                                      "
                                        @mouseenter="showAttrBin(cna, bin)"
                                        @mouseleave="hiddenAttrBin(cna, bin)"
                                ></polygon>
                                <line
                                        :x1="0"
                                        :x2="0"
                                        y1="0"
                                        y2="10"
                                        stroke-width="2px"
                                        :stroke="BaseColorMap['black']"
                                ></line>
                                <text
                                        x="0"
                                        y="-12"
                                        text-anchor="middle"
                                        style="font-size: 12px"
                                        v-show="AttrBinRangeShowMap[cna][bin] == true"
                                >
                                    {{ bin }}
                                </text>
                            </g>
                            <text x="0" y="50" text-anchor="start" class="greySvgText">
                                {{ AttrBinRangeMap[cna][0] }}
                            </text>
                            <text x="195" y="50" text-anchor="middle" class="greySvgText">
                                {{ AttrBinRangeMap[cna][AttrBinRangeMap[cna].length - 1] }}
                            </text>
                        </g>
                        <g v-else>
                            <g
                                    :key="i + 1"
                                    v-for="(bin, i) in AttrBinRangeMap[cna]"
                                    :transform="`translate(${
                  (200 / (AttrBinRangeMap[cna].length + 1)) * (i + 1)
                }, 25)`"
                            >
<!--                                <polygon-->
<!--                                        points="-8,0 8,0 0,13"-->
<!--                                        transform="translate(0, -10)"-->
<!--                                        @click="reverseQueryBin(cna, bin)"-->
<!--                                        :stroke="BaseColorMap['grey-normal']"-->
<!--                                        :fill="-->
<!--                    AttrQueryBinRangeMap[cna].includes(bin)-->
<!--                      ? BaseColorMap['grey-normal']-->
<!--                      : BaseColorMap['white']-->
<!--                  "-->
<!--                                        @mouseenter="showAttrBin(cna, bin)"-->
<!--                                        @mouseleave="hiddenAttrBin(cna, bin)"-->
<!--                                ></polygon>-->
                                <line
                                        :x1="0"
                                        :x2="0"
                                        y1="0"
                                        y2="10"
                                        stroke-width="2px"
                                        :stroke="BaseColorMap['black']"
                                ></line>
                                <text
                                        :x="Object.keys(AttrBinRangeMap[cna]).length <=2 ? 0 : -5"
                                        :y="Object.keys(AttrBinRangeMap[cna]).length <=2 ? 25 : 30"
                                        text-anchor="middle"
                                        :transform="Object.keys(AttrBinRangeMap[cna]).length <=2 ? '' : 'rotate(-20)'"
                                        class="greySvgText"
                                >
                                    {{ bin }}
                                </text>
                            </g>
                        </g>
                    </svg>
                    <!-- <vue-slider

            class="AttrBinRangeSlider"
            :min="AttrRangeMap[cna][0]"
            :max="AttrRangeMap[cna][1]"
            v-model="AttrBinRangeMap[cna]"
            :tooltip-formatter="formatter"
            :dot-options="dotOptions[cnaIdx]"
          ></vue-slider> -->
                    <!-- 类别型 -->
                    <!-- <el-button type="primary" @click="AddBreakPoint(cna)"
          >add break point</el-button
        > -->
                </div>
                <el-select
                        v-if="AddState"
                        v-model="TempAttr"
                        class="m-2"
                        placeholder="Select"
                        style="width: 130px"
                        @change="ConfirmAddAttr"
                >
                    <el-option
                            v-for="item in DatasetColumns.filter(
              (d) => !CurExeQuery.includes(d)
            )"
                            :key="item"
                            :label="item"
                            :value="item"
                    />
                </el-select>
                <!-- <el-button v-if="AddState" @click="ConfirmAddAttr"></el-button> -->
                <el-button style="margin: 20px 40% 10px 40%" @click="AddNewAttr">
                    <el-icon style="width: 40px; height: 40px"><Plus /></el-icon>
                </el-button>

                <div class="SubmitRow">
                    <div class="FlexRow" style="justify-content: space-between">
                        <div>
                            <span>&epsilon;: </span>
                            <el-input
                                    v-model="CurQueryEpsilonInput"
                                    class="CurQueryEpsilonInput"
                            ></el-input>
                        </div>
                        <el-button
                                type="primary"
                                @click="QuerySimulate"
                                :class="{ SimulateState: CurSimulateState }"
                        >Simulate</el-button
                        >
                        <el-button
                                type="primary"
                                @click="QueryIssue"
                                :class="{ IssueState: CurIssueState }"
                                :disabled="CurIssueState"
                        >Issue</el-button
                        >
                    </div>
                </div>
            </div>
            <el-divider border-style="dashed" class="TextDivider" />

            <div class="QueryTemplateBottom">
                <div class="SubHeading">Recommendations</div>
                <div class="FlexRow">
                    <div class="SubSubHeading">Exploration strategy</div>
                    <div class="SubSubHeading" style="margin-left: 60px">
                        Data request list
                    </div>
                </div>
                <el-scrollbar height="620px" always="true">
                    <div
                            v-for="(qs, i) in QueryStrategyList"
                            :key="qs"
                            :class="{
              FlexRow: true,
              QueryStrategyItem: true,
            }"
                    >
                        <svg class="QueryStrategyItemSvg" :id="`QueryStrategyItemSvg${i}`">
                            <g class="container"></g>
                            <g class="nodeContainer"></g>
                            <g transform="translate(-50, 0)">
                                <rect
                                        x="52"
                                        y="0"
                                        width="135"
                                        :height="135"
                                        fill="none"
                                        :stroke="BaseColorMap['grey-light']"
                                        stroke-dasharray="3 2"
                                        stroke-width="2px"
                                ></rect>
                            </g>
                            <!-- <text
            x="10"
            :y="20 + 40 * qIdx"
            v-for="(query, qIdx) in QueryStrategyList[+i]"
            :key="query"
          >
            {{ query }}
          </text>
          <text x="10" :y="40 + 40 * 1">
            {{
              StrategySpecific[+i]["QuerySeq"] +
              "\n" +
              StrategySpecific[+i]["QueryEpsilonList"] +
              "\n" +
              StrategySpecific[+i]["QueryGranularity"]
            }}
          </text> -->
                        </svg>
                        <el-scrollbar max-height="140px" class="queryScroll" always="true">
                            <div
                                    v-for="(query, queryIdx) in QueryStrategyList[+i]"
                                    :key="query"
                                    class="blueBg FlexRow"
                                    :class="{
                  CurStrategyQuery:
                    +i === CurQueryStrategyIdx && +queryIdx === CurQueryIdx,
                  FlexRow: true,
                  blueBg: true,
                }"
                                    @click="chooseCurQuery(+i, +queryIdx)"
                            >
                                <!-- svg part -->
                                <div class="svgpart">
                                    <svg :id="`querySpace${queryIdx}`">
                                        <rect
                                                x="5"
                                                y="5"
                                                width="55"
                                                height="55"

                                                :fill="BaseColorMap['white']"
                                                stroke="none"
                                        ></rect>
                                        <text
                                                x="30"
                                                y="50"
                                                fill="#666"
                                                text-anchor="middle"
                                                v-if="StrategySpecific[+i]['QueryEpsilonList'] && isSensitiveQuery(query)"
                                        >
                                            ε:
                                            {{ StrategySpecific[+i]["QueryEpsilonList"][+queryIdx] }}
                                        </text>
                                    </svg>
                                </div>
                                <!-- text part -->
                                <div class="textpart">
                                    <div
                                            x="30"
                                            :y="40 + 20 * aIdx"
                                            v-for="(attr, aIdx) in query"
                                            :key="attr"
                                    >
                                        {{ attr }}
                                    </div>
                                </div>
                            </div>
                        </el-scrollbar>
                    </div>
                </el-scrollbar>
            </div>
        </div>
        <!-- <div class="QueryStrategyBody ColorBox">

    </div> -->
    </div>

    <div class="RightPart">
        <!-- 可视编码与展示部分 -->
        <!-- <div class="MainHeading">Visual Query</div> -->
        <!-- <div>
        Current private budget:
        <el-input
          v-model="CurQueryListEpsilonThreshold"
          placeholder="placeholder"
        ></el-input>
      </div> -->
        <!-- <el-button type="primary" @click="QueryConfirm"
        >Query simulation</el-button
      >
      <el-button type="primary" @click="QueryConfirmWithEpsilon"
        >Query confirm</el-button
      > -->
        <!-- <div>查询顺序{{ QuerySeq }}</div>
      <div>预算分配{{ QueryEpsilonList }}</div>
      <div>查询粒度{{ QueryGranularity }}</div> -->

        <div class="ChartPart ColorBox">
            <div class="MainChart">
                <div class="FlexRow">
                    <div class="MainHeading">
                        Uncertainty Illustration {{ CurQueryState }}
                    </div>
                    <el-switch
                            style="margin-left: auto"
                            v-model="ShowMode"
                            size="middle"
                            active-text="Feedback summary"
                            @change="showSummary"
                            inactive-text="Current request"
                    />
                </div>
                <el-divider border-style="dashed" class="TextDivider" />
                <svg id="QueryResultChart">
                    <g class="content"></g>
                    <g class="legend">
                        <g
                                class="errorbarLegend"
                                transform="translate(590, 20)"
                                v-if="CurHeatMapColorScaleLegendList.length > 0"
                        >
                            <rect
                                    x="5"
                                    y="10"
                                    width="25.125"
                                    height="66"
                                    :fill="BaseColorMap['grey-normal']"
                                    fill-opacity="0.5"
                                    stroke="none"
                            ></rect>
                            <line
                                    x1="17.5625"
                                    x2="17.5625"
                                    y1="26.76146907866098"
                                    y2="-6.76146907866098"
                                    :stroke="BaseColorMap['grey-normal']"
                                    stroke-width="2px"
                            ></line>
                            <line
                                    x1="12.5375"
                                    x2="22.5875"
                                    y1="26.76146907866098"
                                    y2="26.76146907866098"
                                    :stroke="BaseColorMap['grey-normal']"
                                    stroke-width="2px"
                            ></line>
                            <line
                                    x1="12.5375"
                                    x2="22.5875"
                                    y1="-6.76146907866098"
                                    y2="-6.76146907866098"
                                    :stroke="BaseColorMap['grey-normal']"
                                    stroke-width="2px"
                            ></line>
                        </g>

                        <g
                                class="ColorLegend"
                                transform="translate(300, 50)"
                                v-if="CurHeatMapColorScaleLegendList.length > 0"
                        >
                            <g transform="translate(410, -30)">
                                <rect
                                        v-for="(d, i) in CurHeatMapColorScaleLegendList"
                                        :key="d"
                                        :x="i * 2"
                                        y="0"
                                        width="4"
                                        height="10"
                                        :fill="CurHeatMapColorScale(d)"
                                ></rect>
                                <text x="50" y="-5" text-anchor="middle" class="legendMText">
                                    Count
                                </text>
                                <text x="-10" y="10" text-anchor="end" class="legendMText">
                                    {{ CurHeatMapColorScaleLegendList[0].toFixed(0) }}
                                </text>
                                <text x="110" y="10" class="legendMText">
                                    {{
                                    CurHeatMapColorScaleLegendList[
                                    CurHeatMapColorScaleLegendList.length - 1
                                        ].toFixed(0)
                                    }}
                                </text>
                            </g>
                            <g class="innerG" transform="translate(450, 0)">
                                <g transform="translate(0, 10)">
                                    <g transform="scale(2.0) translate(-7, -13)">
                                        <rect
                                                x="0"
                                                y="0"
                                                width="26.049999999999997"
                                                height="26.049999999999997"
                                                :stroke="BaseColorMap['white']"
                                                stroke-width="1px"
                                                fill="rgb(226, 244, 229)"
                                        ></rect>
                                        <polygon
                                                class="rectTRUE"
                                                points="0,0 17.69021426126103,0 0,26.049999999999997"
                                                :stroke="BaseColorMap['white']"
                                                stroke-width="1px"
                                                fill="rgb(207, 236, 211)"
                                        ></polygon>
                                        <polygon
                                                class="rectTRUE"
                                                points="26.049999999999997,0 26.049999999999997,26.049999999999997 8.359785738738967,26.049999999999997"
                                                :stroke="BaseColorMap['white']"
                                                stroke-width="1px"
                                                fill="rgb(245, 251, 246)"
                                        ></polygon>
                                    </g>
                                    <line
                                            x1="-30"
                                            x2="-5"
                                            y1="0"
                                            y2="0"
                                            :stroke="BaseColorMap['grey-normal']"
                                            stroke-width="2px"
                                    ></line>
                                    <line
                                            x1="30"
                                            x2="55"
                                            y1="0"
                                            y2="0"
                                            :stroke="BaseColorMap['grey-normal']"
                                            stroke-width="2px"
                                    ></line>
                                    <text
                                            x="-40"
                                            y="27"
                                            transform="rotate(-90)"
                                            :fill="BaseColorMap['grey-normal']"
                                            style="font-size: 40px"
                                    >
                                        {
                                    </text>
                                </g>

                                <text x="-80" y="15" text-anchor="middle" class="legendMText">
                                    Upper bound
                                </text>
                                <text x="-220" y="20" text-anchor="middle" class="legendMText">
                                    CI (95%):
                                </text>
                                <text x="-140" y="90" text-anchor="middle" class="legendMText">
                                    in bars
                                </text>
                                <text x="10" y="90" text-anchor="middle" class="legendMText">
                                    in grids
                                </text>
                                <text x="107" y="15" text-anchor="middle" class="legendMText">
                                    Lower bound
                                </text>
                                <text x="-50" y="45" text-anchor="middle">
                                    <tspan x="15" dy="1.2em" class="legendMText">Length/2</tspan>
                                </text>
                            </g>
                        </g>
                    </g>
                </svg>
                <div class="AttrFilterPanel">
                    <div class="NosieModeChange FlexRow">
                        <div>Noise mode:</div>
                        <el-switch
                                style="margin-left: 10px"
                                v-model="noiseMode"
                                size="middle"
                                active-text="Include"
                                inactive-text="Remove"
                        />
                        <el-button
                                @click="ResetHeatMap"
                                type="primary"
                                v-if="!noiseMode"
                                style="margin-left: 40px"
                        >Reset</el-button
                        >
                    </div>

                    <div class="FlexRow">
                        <div style="line-height: 32px">Filter: attribute-value</div>

                    </div>

                    <div class="FlexRow">
                        <el-select
                                v-model="CurFilterAttr"
                                clearable
                                v-if="PreExeQuery.length > 1"
                                placeholder="Select"
                                size="middle"
                                style="width: 100px;"
                        >
                            <el-option

                                    v-for="item in ShowMode ? TotalQueryAttrs : PreExeQuery"
                                    :key="item"
                                    :label="item"
                                    :value="item"
                            />
                        </el-select>
                        <el-select
                                v-model="CurFilterAttrRange"
                                clearable
                                v-if="AttrBinRangeMap[CurFilterAttr]"
                                placeholder="Select"
                                size="middle"
                                style="width: 100px; margin-left: 15px"
                        >
                            <el-option
                                    v-for="item in CurFilterAttrRangeList"
                                    :key="item"
                                    :label="item"
                                    :value="item"
                            />
                        </el-select>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import * as d3 from "d3";
import hull from "d3-hull"; // 注意这里的引入方式
import draggable from "vuedraggable";
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";
import axios from "axios";
import { vShow } from "vue";

export default {
    name: "New",
    components: { draggable, VueSlider },
    data() {
        return {
            BaseColorMap: {
                "blue-normal": "rgba(52, 152, 219,1.0)",
                "blue-normal-opacity": "rgba(52, 152, 219,0.5)",
                "blue-normal-oopacity": "rgba(52, 152, 219,0.3)",
                "red-sensitive": "rgb(234,120,119)",
                "red-sensitive-opacity": "rgba(234,120,119, 1.0)",

                "grey-light": "rgb(220,220,220)",
                "grey-normal": "rgb(150,150,150)",
                "grey-normal-opacity": "rgba(150,150,150, 0.5)",
                "grey-deep": "rgb(176,176,176)",
                "white": "rgb(255,255,255)",
                "black": "rgb(0,0,0)",
                'orange': "rgba(250, 130, 49,1.0)",
                "green": "rgba(92, 191, 107,1.0)",
            },
            DataBaseList: ["Customer Life Time value", "National Health and Nutrition Examination Survey"],
            CurDatabase: "National Health and Nutrition Examination Survey",
            BaseEpsilonMap: {
                'Customer Life Time value': 1.0,
                'National Health and Nutrition Examination Survey': 1.0
            },
            TotalEpsilonMap: {
                'Customer Life Time value': 1.0,
                'National Health and Nutrition Examination Survey': 1.0
            },
            CurEpsilon: 1.0,
            CurVisTypeList: ["histogram", "heatmap"],
            CurVisType: "heatmap",
            QueryContentOption: ["#COUNT", "xxx"],
            CurQueryContent: "#COUNT",
            CurSimulateResult: [],

            Dataset: [],
            DatasetColumns: [],
            ColumnDbClickMap: {},
            AttrTypeMap: [], // A: categorical  #: numerical  T: temporal
            AttrRangeMap: [],
            minAttrGranularityList: [],
            AttrBinRangeMap: {},
            AttrSensitive: {},
            CurQuery: [],

            // CurQueryListEpsilonThreshold: 1.0,
            StrategyEpsilonDistributeMap: {},
            CurQueryList: [],
            // QueryAttrList: computed
            // QueryRegionList: computed
            CurNumericalAttrList: [],
            QueryStrategyList: [],
            CurQueryStrategyIdx: 0,
            CurQueryIdx: 0,
            // CurQuery: computed
            QuerySimulationModolList: ["up", "down"],
            isSimulation: true,
            NoiseMatrix: [],
            NoiseMap: {},
            // CurQueryEpsilon: 0,

            QueryHistory: [],

            SvgWidth: 800,
            SvgHeight: 400,

            // 推荐结果
            StrategySpecific: [],
            // QuerySeq: [],
            // QueryEpsilonList: [],
            // QueryGranularity: [],

            CurInputText: "",
            CurLineName: "",
            CurLineNonSensitiveAttr: "",
            CurLineSensitiveAttr: "",
            ShowCorrInput: false,
            CorrQueryMap: {},
            CurHistogramAttr: "",
            SensitiveAttrSimulate: {},

            rectWHMap: {},
            CurHeatMapColorScale: {},
            // IsModifyColorScale: false,
            CurFilterAttr: "",
            CurFilterAttrRange: "",
            formatter: (d) => d / 1000 + "k",
            AttrIntentMap: {},
            NoiseInclideModel: ["include", "remove"],
            noiseMode: true,
            CurQueryEpsilonInput: 0,
            CurThisNodeName: "",
            CurExeQuery: [],

            SimulatedCorrelationMap: {},
            VerifiedCorrelationMap: {},
            AddState: false,
            TempAttr: "",
            CurQueryState: "",
            CurExDataset: [],
            AttrQueryBinRangeMap: {},
            simulateDataRecord: {},
            VerifiedDataRecord: {},
            AttrDistributionYscaleMap: {},
            AttrBinRangeShowMap: {},
            ShowMode: false,
            TotalQuerys: [],
            TotalQueryAttrs: [],
            TotalQueryResults: {},
            NoiseCountMap: {},
            EpsilonMap: {},
            NodeMinY: {},

            CurSimulateState: false,
            CurIssueState: false,
            PreQueryEpsilon: 0,
            PreExeQuery: [],
            specialAttrList: [],
            isFilter: false,
            AttrMessMap: {},
            ExplorationProgressVal: 0,
            OldExplorationProgressVal: 0,
            ExplorationProgressMarks: d => d%100===0,
            // FilterSensitive: false,
        };
    },
    computed: {
        QueryRegionList() {
            let singleAttrQuery = this.CurQueryList.filter((d) => d.length === 1);
            let doubleAttrQuery = this.CurQueryList.filter((d) => d.length > 1);
            let edgeRegions = this.connectedRegions(doubleAttrQuery);
            let singleAttrRegions = [];
            for (let saq of singleAttrQuery) {
                let isIncludes = false;
                for (let daq of doubleAttrQuery) {
                    if (daq.includes(saq)) {
                        isIncludes = true;
                        break;
                    }
                }
                if (!isIncludes) {
                    singleAttrRegions.push([[saq]]);
                }
            }
            return edgeRegions.concat(singleAttrRegions);
        },
        // QueryStrategyList() {
        //   let strategy1 = [];
        //   for (let QR of this.QueryRegionList) {
        //     let newQuery = [];
        //     for (let query of QR) {
        //       newQuery = newQuery.concat(query);
        //     }
        //     strategy1.push([...new Set(newQuery)]);
        //   }
        //   this.CurQueryStrategyIdx = 0;
        //   let strategy2 = [];
        //   for (let QR of this.QueryRegionList) {
        //     strategy2 = strategy2.concat(QR);
        //   }
        //   this.StrategyEpsilonDistributeMap[0] = new Array(strategy1.length).fill(
        //     this.CurQueryListEpsilonThreshold / strategy1.length
        //   );
        //   this.StrategyEpsilonDistributeMap[1] = new Array(strategy2.length).fill(
        //     this.CurQueryListEpsilonThreshold / strategy2.length
        //   );
        //   return [strategy1, strategy2];
        // },
        QueryAttrList() {
            let ret = [];
            for (let query of this.CurQueryList) {
                for (let attr of query) {
                    ret.push(attr);
                }
            }
            ret = [...new Set(ret)];
            return ret;
        },
        // CurQuery() {
        //     let len = this.QueryStrategyList.length;
        //     let curStrategy = this.QueryStrategyList[this.CurQueryStrategyIdx];
        //     if (curStrategy == undefined || curStrategy.length === 0) {
        //         this.CurExeQuery = [];
        //         return [];
        //     } else {
        //         this.CurExeQuery = JSON.parse(
        //             JSON.stringify(curStrategy[this.CurQueryIdx])
        //         );
        //         return curStrategy[this.CurQueryIdx];
        //     }
        // },
        CurEpsilonNoiseList() {
            let e;
            if(this.CurQueryEpsilonInput === 0) {
                e = this.PreQueryEpsilon
            }
            else {
                e = this.CurQueryEpsilonInput;
            }
            let b = 1 / e;
            let ret = [];
            for (let i = 0; i < 10000; i++) {
                ret.push(this.generateLaplaceNoise(0, b));
            }
            return ret;
        },
        FilterSensitive() {
          return this.AttrSensitive[this.CurFilterAttr] === true && this.CurFilterAttrRange !== '';
        },
        CurFilterAttrRangeList() {
            let attrRange = this.AttrBinRangeMap[this.CurFilterAttr];
            if (attrRange) {
                if (typeof attrRange[0] === "number") {
                    let ret = [];
                    for (let i in attrRange) {
                        if (+i === 0) continue;
                        ret.push(attrRange[+i - 1] + "~" + attrRange[+i]);
                    }
                    return ret;
                } else {
                    return attrRange;
                }
            } else {
                return attrRange;
            }
        },
        CurHeatMapColorScaleLegendList() {
            // 空
            if (typeof this.CurHeatMapColorScale === "object") {
                return [];
            } else {
                let domain = this.CurHeatMapColorScale.domain();
                return [...d3.range(domain[0], domain[2], (domain[2] - domain[0]) / 50), domain[2]];
            }
        },
        CurNumericalQuery() {
            return this.CurNumericalAttrList.filter((d) =>
                this.CurExeQuery.includes(d)
            );
        },
        // dotOptions() {
        //   let ret = [];
        //   for (let cna of this.CurNumericalQuery) {
        //     let temp = [];
        //     for (let i in this.AttrBinRangeMap[cna]) {
        //       if (+i === 0 || +i === this.AttrBinRangeMap[cna].length - 1) {
        //         temp.push({
        //           tooltip: "always",
        //         });
        //       } else {
        //         temp.push({
        //           tooltip: "active",
        //         });
        //       }
        //     }
        //     ret.push(temp);
        //   }
        //   console.log("dotOptions", ret);
        //   return ret;
        // },
        CurEpsilonChange({ StrategySpecific, CurQueryStrategyIdx }) {
            return { StrategySpecific, CurQueryStrategyIdx };
        },
        CurFilterChange({ CurFilterAttr, CurFilterAttrRange }) {
            return { CurFilterAttr, CurFilterAttrRange };
        },
        SimulationAndIssueStateChange() {
            return this.TotalEpsilonMap[this.CurDatabase] - this.CurQueryEpsilonInput >= 0;
        },
        StrategyChange({ QueryStrategyList, CurQueryStrategyIdx, CurQueryIdx }) {
            return { QueryStrategyList, CurQueryStrategyIdx, CurQueryIdx }
        },
    },
    watch: {
        StrategyChange: {
          handler() {
              let len = this.QueryStrategyList.length;
              let curStrategy = this.QueryStrategyList[this.CurQueryStrategyIdx];
              this.CurSimulateState = false;
              if (curStrategy == undefined || curStrategy.length === 0) {
                  this.CurExeQuery = [];
                  this.CurQuery = [];
              } else {
                  this.CurExeQuery = JSON.parse(
                      JSON.stringify(curStrategy[this.CurQueryIdx])
                  );
                  this.CurQuery = curStrategy[this.CurQueryIdx];
              }
              let isSensitiveQuery = this.isSensitiveQuery(this.CurQuery);
              if(!isSensitiveQuery) {
                  this.CurQueryEpsilonInput = 0;
              }

          },
          deep: true,
        },
        CurFilterChange(newV, oldV) {
            if(newV['CurFilterAttr'] !== oldV['CurFilterAttr']) {
                if(newV['CurFilterAttr'] === '') {
                    this.CurFilterAttrRange = ''
                }
                this.$nextTick(() =>{
                    this.CurFilterAttrRange = this.CurFilterAttrRangeList[0];
                })
                return
            }
            if(!this.ShowMode) {
                if (this.CurFilterAttrRange !== "") {
                    // 执行过滤
                    let isN = this.CurFilterAttrRange.split("~").length > 1 ? true : false;
                    let [rangeL, rangeR] = this.CurFilterAttrRange.split("~").map(
                        (d) => +d
                    );
                    this.CurExDataset = this.Dataset.filter((d) => {
                        if (isN) {
                            return (
                                d[this.CurFilterAttr] > rangeL && d[this.CurFilterAttr] < rangeR
                            );
                        } else {
                            return d[this.CurFilterAttr] == this.CurFilterAttrRange;
                        }
                    });
                    this.QueryConfirm(this.PreExeQuery, this.PreQueryEpsilon);
                }
                else {
                    this.CurExDataset = this.Dataset.map(d => d);
                    this.QueryConfirm(this.PreExeQuery, this.PreQueryEpsilon);
                }
            } else {
                // summary mode
                let isN = this.CurFilterAttrRange.split("~").length > 1 ? true : false;
                let [rangeL, rangeR] = this.CurFilterAttrRange.split("~").map(
                    (d) => +d
                );
                this.CurExDataset = this.Dataset.filter((d) => {
                    if (isN) {
                        return (
                            d[this.CurFilterAttr] > rangeL && d[this.CurFilterAttr] < rangeR
                        );
                    } else {
                        return d[this.CurFilterAttr] == this.CurFilterAttrRange;
                    }
                });
                if (this.CurFilterAttrRange !== "") {
                    this.isFilter = true;
                    this.showSummary();
                } else {
                    this.isFilter = false;
                    this.showSummary();
                }
            }
        },
        QueryAttrList(newV) {
            let CurNumericalAttrList = this.QueryAttrList.filter(
                (d) => this.AttrTypeMap[d] === "#"
            );

            this.CurNumericalAttrList = CurNumericalAttrList;
        },
        noiseMode(newV) {
            this.QueryConfirm(this.PreExeQuery);
        },
        QueryStrategyList: {
            handler(newValue, oldValue) {
                this.$nextTick(() => {
                    for (let idx in newValue) {
                        let svg = d3.select(`#QueryStrategyItemSvg${+idx}`);
                        svg.selectAll(".container *").remove();
                        let container = svg.select(".container");
                        let nodeContainer = svg.select(".nodeContainer");
                        svg.selectAll(".nodeContainer *").remove();
                        // svg.append('text')
                        //   .attr('x', 20)
                        //   .attr('y', 20)
                        //   .text(JSON.stringify(this.QueryStrategyList[+idx]))
                        let queryStrategy = newValue[+idx];
                        let LinkData = [];
                        let NodeData = [];
                        // 获取 base query -- linkData 和 nodeData
                        for (let query of queryStrategy) {
                            NodeData = NodeData.concat(query);
                            let len = query.length;
                            if (len === 1) {
                                continue;
                            } else if (len === 2) {
                                LinkData.push(query);
                            } else {
                                for (let rawQuery of this.CurQueryList) {
                                    if (
                                        query.includes(rawQuery[0]) &&
                                        query.includes(rawQuery[1])
                                    ) {
                                        LinkData.push([rawQuery[0], rawQuery[1]]);
                                    }
                                }
                            }
                        }
                        NodeData = Array.from(new Set([...NodeData]));
                        NodeData = NodeData.map((d) => ({ id: d }));
                        LinkData = LinkData.map((d) => ({ source: d[0], target: d[1] }));
                        // 绘制查询图
                        const simulation = d3
                            .forceSimulation(NodeData)
                            .force(
                                "link",
                                d3.forceLink(LinkData).id((d) => d.id)
                            )
                            .force("charge", d3.forceManyBody())
                            .force("center", d3.forceCenter(50, 50));

                        // 绘制边
                        const link = container
                            .selectAll("line")
                            .data(LinkData)
                            .enter()
                            .append("line")
                            .style("stroke", this.BaseColorMap["grey-normal"])
                            .style("stroke-width", 2);

                        // 绘制节点
                        const node = nodeContainer
                            .selectAll("circle")
                            .data(NodeData)
                            .enter()
                            .append("circle")
                            .attr("r", 10)
                            .attr("fill", this.BaseColorMap["white"])
                            .attr("stroke-width", "3px")
                            .attr("stroke", (d) =>
                                this.AttrSensitive[d.id]
                                    ? this.BaseColorMap["red-sensitive"]
                                    : this.BaseColorMap["blue-normal"]
                            );

                        simulation.on("tick", () => {
                            link
                                .attr("x1", (d) => d.source.x)
                                .attr("y1", (d) => d.source.y)
                                .attr("x2", (d) => d.target.x)
                                .attr("y2", (d) => d.target.y);

                            node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
                        });

                        // 确定 query node 的位置
                        let BoundingClientRect = d3
                            .select(".QueryContainer rect")
                            .node()
                            .getBoundingClientRect();
                        let { width: rawWidth, height: rawHeight } = BoundingClientRect;
                        let CurWH = 135;
                        node.attr("a", (d) => {
                            let translateStr = d3
                                .select(`.DBAttrBody .DBAttrItem[name='${d.id}']`)
                                .attr("transform");
                            const matches = translateStr.match(
                                /translate\((-?[\d.]+),(-?[\d.]+)\)/
                            );
                            console.log([+matches[1], +matches[2]]);
                            [d.fx, d.fy] = [
                                ((+matches[1] + 40) / rawWidth) * CurWH,
                                ((+matches[2] - 200) / rawHeight) * CurWH,
                            ];
                            [d.x, d.y] = [d.fx, d.fy]
                            return +matches[1];
                        });

                        //用凸包表示查询
                        // setTimeout(() => {
                        let curve = d3.line().curve(d3.curveCardinalClosed.tension(0.2));
                        let hullg = svg.select(".container");
                        let hullNodeData = [];
                        for (let queryIdx in queryStrategy) {
                            let temp = [];
                            for (let attr of queryStrategy[+queryIdx]) {
                                temp.push(NodeData.find((d) => d.id === attr));
                            }
                            hullNodeData.push(temp);
                        }
                        let svgHulls = hullg
                            .selectAll(".hull")
                            .data(convexHulls(hullNodeData, LinkData))
                            .enter()
                            .append("path")
                            .attr("id", (d, i) => {
                                return hullNodeData[i].map((d) => d.id).join("||");
                            })
                            .attr("class", "hull")
                            .attr("opacity", 0.3)
                            .style("fill", this.BaseColorMap["grey-normal"])
                            .attr("d", (d) => curve(d.path))
                            .each(function (d, i) {
                                d3.select(svg.node().nextElementSibling)
                                    .select(`#querySpace${i}`)
                                    .insert(() => this.cloneNode(true))
                                    .attr("transform", "scale(0.33)translate(10, 10)");
                            });
                        // }, 2000);
                        function convexHulls(nodes, edges) {
                            const offset = 15;
                            let hulls = {};
                            let gName = 0;
                            for (let k = 0; k < nodes.length; ++k) {
                                let Gnodes = nodes[k];
                                let l = hulls[k] || (hulls[k] = []);
                                for (let n of Gnodes) {
                                    l.push([n.x - offset, n.y - offset]);
                                    l.push([n.x - offset, n.y + offset]);
                                    l.push([n.x + offset, n.y - offset]);
                                    l.push([n.x + offset, n.y + offset]);
                                }
                            }
                            // create convex hulls
                            let hullset = [];
                            for (let i in hulls) {
                                hullset.push({ group: i, path: d3.polygonHull(hulls[i]) });
                            }
                            return hullset;
                        }
                    }
                });
            },
            deep: true, // 设置 deep 为 true，以便深度监视对象内部的变化
        },
        CurQueryList: {
            handler(newValue, oldValue) {
                // 策略推荐
                axios({
                    method: "post",
                    url: "http://127.0.0.1:8000/RL/StrategyRecommend/",
                    data: {
                        queryList: newValue,
                    },
                }).then((response) => {
                    let data = response.data;
                    this.QueryStrategyList = data.strategyList;
                    this.StrategySpecific = [];
                    for (let [idx, queryStategy] of Object.entries(
                        this.QueryStrategyList
                    )) {
                        this.CurSimulateResult = [];
                        this.StrategySpecific.push({});
                        let PromiseList = [];
                        for (let queryAttrName of queryStategy) {
                            PromiseList.push(
                                this.executeQuery(queryAttrName, this.CurQueryContent, true)
                            );
                        }
                        Promise.all(PromiseList).then((data) => {
                            this.CurSimulateResult = data.map((d) => d[0]);

                            // 预算推荐
                            axios({
                                method: "post",
                                url: "http://127.0.0.1:8000/RL/RLRecommend/",
                                data: {
                                    queryList: queryStategy,
                                    rawQueryList: this.QueryStrategyList[0],
                                    isRawQuery: +idx === 0,
                                    AttrSensitive: this.AttrSensitive,
                                    attrTypeMap: this.AttrTypeMap,
                                    simulateResult: this.CurSimulateResult,
                                    epsilon: this.TotalEpsilonMap[this.CurDatabase],
                                    'ExplorationProgressVal': this.ExplorationProgressVal,
                                    'N': this.CurExDataset.length,
                                },
                            }).then((response) => {
                                let data = response.data;
                                if (+idx === this.CurQueryStrategyIdx) {
                                    this.CurQueryIdx = data.QuerySeq[0];
                                }
                                this.StrategySpecific[+idx] = {
                                    QuerySeq: data.QuerySeq,
                                    QueryEpsilonList: data.QueryEpsilonList,
                                    QueryGranularity: data.QueryGranularity,
                                };
                                console.log(this.StrategySpecific);
                            });
                        });
                    }
                });
            },
            deep: true, // 设置 deep 为 true，以便深度监视对象内部的变化
        },
        CurQueryEpsilonInput: {
          handler(newV) {
              this.CurSimulateState = false;
          }
        },
        CurEpsilonChange: {
            handler(newV) {
                if (
                    this.StrategySpecific[this.CurQueryStrategyIdx] &&
                    this.StrategySpecific[this.CurQueryStrategyIdx]["QueryEpsilonList"]
                ) {
                    this.CurQueryEpsilonInput =
                        this.StrategySpecific[this.CurQueryStrategyIdx]["QueryEpsilonList"][
                            this.CurQueryIdx
                            ];
                }
            },
            deep: true,
        },
        SimulationAndIssueStateChange: {
            handler(newV) {
                if(this.SimulationAndIssueStateChange === false) {
                    this.CurIssueState = true;
                }
                else {
                    this.CurIssueState = false;
                }

            },
            deep: true,
        },
    },
    methods: {
        // 通用类函数
        isSensitiveQuery(query) {
            let isSensitiveQuery = false;
            for(let attr of query) {
                if(this.AttrSensitive[attr]) {
                    isSensitiveQuery = true;
                }
            }
            return isSensitiveQuery;
        },
        roundToHighestPlace(number, preserveDigits) {
            // 将数字转换为字符串以便处理
            let numString = number.toString();
            let firstNonZeroIndex = 0;

            // 计算要保留的最高位数
            let preservedDigits = Math.min(
                preserveDigits,
                numString.length - firstNonZeroIndex
            );

            let preservedValue = parseInt(
                numString.substring(
                    firstNonZeroIndex,
                    firstNonZeroIndex + preservedDigits
                )
            );

            let testValue = parseInt(numString[firstNonZeroIndex + preservedDigits]);

            // 如果第一个非零数字大于等于5，则向上取整
            if (testValue >= 5 * Math.pow(10, preservedDigits - 1)) {
                return (
                    (preservedValue + 1) *
                    Math.pow(10, numString.length - firstNonZeroIndex - preservedDigits)
                );
            } else {
                // 否则，返回保留的最高位数的值
                return (
                    preservedValue *
                    Math.pow(10, numString.length - firstNonZeroIndex - preservedDigits)
                );
            }
        },

        laplacePDF(x, mu, b) {
            return (1 / (2 * b)) * Math.exp(-Math.abs(x - mu) / b);
        },
        // 数值逼近法计算四分位点
        calculateQuantile(mu = 0, b, percentile) {
            let step = 0.001; // 逼近的步长
            let x = mu; // 从均值开始

            let cumulativeProbability = 0;
            while (cumulativeProbability < percentile) {
                cumulativeProbability += step * this.laplacePDF(x, mu, b);
                x += step;
            }
            return x;
        },
        getAllCombinations(groups) {
            const result = [];

            function generateCombinations(current, groupIndex) {
                result.push(current.slice());

                for (let i = groupIndex; i < groups.length; i++) {
                    const currentGroup = groups[i];

                    for (let j = 0; j < currentGroup.length; j++) {
                        current.push(currentGroup[j]);
                        generateCombinations(current, i + 1);
                        current.pop();
                    }
                }
            }

            generateCombinations([], 0);
            return result;
        },
        getNoiseMatrix(mu, b) {
            let NoiseMatrix = [];
            let CurQuery = this.CurQuery;
            let NoiseNum = 1;
            for (let attr of CurQuery) {
                if (this.AttrTypeMap[attr] === "A") {
                    NoiseNum *= this.AttrRangeMap[attr].length;
                } else {
                    NoiseNum *= this.AttrBinRangeMap[attr].length - 1;
                }
            }
            for (let i = 0; i < NoiseNum; i++) {
                NoiseMatrix.push(this.generateLaplaceNoise(mu, b));
            }
            return NoiseMatrix;
        },
        getNoiseMap(mu, b) {
            let NoiseMatrix = this.getNoiseMatrix(mu, b);
            // 获取属性类别全组合
            let CategoryList = [];
            for (let [attrI, attr] of Object.entries(this.CurQuery)) {
                let n;
                let categories = [];
                if (this.AttrTypeMap[attr] === "A") {
                    n = this.AttrRangeMap[attr].length;
                } else {
                    n = this.AttrBinRangeMap[attr].length - 1;
                }
                for (let i = 0; i < n; i++) {
                    categories.push(String.fromCharCode(+attrI + 97) + i);
                }
                CategoryList.push(categories);
            }
            let totalCategory = this.getAllCombinations(CategoryList);
            totalCategory.shift(); // 删除空[]
            let NoiseMap = {};
            let highLevelCategory = totalCategory
                .filter((d) => d.length === this.CurQuery.length)
                .map((d) => d.join("-"));
            let lowLevelCategory = totalCategory
                .filter((d) => d.length < this.CurQuery.length)
                .map((d) => d.join("-"));
            for (let idx in NoiseMatrix) {
                NoiseMap[highLevelCategory[+idx]] = NoiseMatrix[+idx];
            }
            let BaseNoiseMapKey = Object.keys(NoiseMap);
            for (let category of lowLevelCategory) {
                let categoryL = category.split("-");
                let temp = BaseNoiseMapKey;
                for (let c of categoryL) {
                    temp = temp.filter((d) => d.includes(c));
                }
                let sum = 0;
                for (let key of temp) {
                    sum += NoiseMap[key];
                }
                NoiseMap[category] = sum;
            }
            console.log(NoiseMap);
            return NoiseMap;
        },
        getMultiNoise(b, count) {
            let ret = 0;
            for (let i = 0; i < count; i++) {
                ret += this.CurEpsilonNoiseList[Math.floor(Math.random() * 10000)];
            }
            return ret;
        },
        generateLaplaceNoise(mu, b) {
            const u = Math.random() - 0.5; // 生成均匀分布的随机数在 [-0.5, 0.5) 范围内
            const laplacianNoise =
                mu - b * Math.sign(u) * Math.log(1 - 2 * Math.abs(u));
            return laplacianNoise;
        },

        connectedRegions(edges) {
            const graph = {};

            // Build the graph
            edges.forEach((edge) => {
                edge.forEach((node) => {
                    if (!graph[node]) {
                        graph[node] = [];
                    }
                });
                graph[edge[0]].push(edge[1]);
                graph[edge[1]].push(edge[0]);
            });

            const visited = new Set();
            const regions = {};
            let currentRegion = 1;

            function dfs(node, region) {
                if (!visited.has(node)) {
                    visited.add(node);
                    regions[node] = region;
                    graph[node].forEach((neighbor) => {
                        dfs(neighbor, region);
                    });
                }
            }

            for (const node in graph) {
                if (!visited.has(node)) {
                    dfs(node, currentRegion);
                    currentRegion++;
                }
            }

            const regionEdges = Array.from({ length: currentRegion - 1 }, () => []);

            edges.forEach((edge) => {
                const region = regions[edge[0]];
                regionEdges[region - 1].push(edge);
            });

            return regionEdges;
        },
        // 接口类函数
        // 执行查询接口
        executeQuery(QueryAttrs, QueryContent, isSimulation) {
            // 单属性 + COUNT 的情况
            if (QueryAttrs.length === 1) {
                let QueryAttrName = QueryAttrs[0];
                let queryRes = this.getQueryRes(
                    QueryAttrName,
                    QueryContent,
                    this.CurExDataset,
                    ""
                );
                let axisAttr = [QueryAttrName, QueryContent];
                return new Promise((resolve) => {
                    resolve([queryRes[1], axisAttr]);
                });
            }
            // 双属性查询的情况
            else if (QueryAttrs.length === 2) {
                return this.executeDbAttrQuery(QueryAttrs, QueryContent, isSimulation);
            } else {
                // 多属性的情况
                return this.executeTriPAttrQuery(QueryAttrs, QueryContent, isSimulation);
            }
        },

        // 绘制查询结果接口
        drawQueryResult(
            queryRes,
            queryAttrs,
            chartContainer,
            [i1, i2],
            padding,
            RectWH,
            [ticks1, ticks2],
            noiseCount,
            epsilon
        ) {
            let isSensitiveQuery = false;
            if(queryAttrs.length === 1) {
                isSensitiveQuery = this.AttrSensitive[queryAttrs[0]]
            }
            else {
                isSensitiveQuery = this.AttrSensitive[queryAttrs[0]] || this.AttrSensitive[queryAttrs[1]];
            }

            let yMax;
            // 将 Map 数据转换为数组
            const data = Object.entries(queryRes);
            // if(isStack) {
            //   SvgWidth -= 50;
            // }

            const svg = chartContainer;
            svg.selectAll("*").remove();
            svg
                .append("rect")
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", ticks1 * (RectWH + 5) + 5)
                .attr("height", ticks2 * (RectWH + 5) + 5)
                .attr("fill", this.BaseColorMap["white"]);
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

            let isNumericalX = this.AttrTypeMap[queryAttrs[0]] == '#';
            let [xScale, tickValues, bandwidthScale, bandwidth] = this.GetScale(
                isNumericalX,
                xDomain,
                [0, ticks1 * (RectWH + 5) + 5],
                true
            );
            if(isNumericalX) {
                tickValues = this.AttrBinRangeMap[queryAttrs[0]];
            }
            // y height scale
            let SvgHeight = ticks2 * (RectWH + 5) + 5;
            let curEpsilon = epsilon ? epsilon : this.CurQueryEpsilonInput;
            if(curEpsilon === 0) curEpsilon = 2;
            let quartileNoise = noiseCount * this.calculateQuantile(
                0,
                1 / curEpsilon,
                0.475
            );
            const yScale = d3
                .scaleLinear()
                .domain([0, yMax + quartileNoise])
                .range([SvgHeight - 5, 10]);

            let container = svg
                .selectAll(".container")
                .data(data)
                .enter()
                .append("g")
                .attr("class", "container");


            let objectContainer = container.filter((d) => typeof d[1] === "object");
            let colorScale = d3.scaleOrdinal(d3.schemeCategory10);
            // 添加坐标轴
            let CurQuery = this.PreExeQuery.filter((d) => d !== this.CurFilterAttr);
            const xAxis = d3.axisBottom(xScale).tickValues(tickValues)
            if(isNumericalX) {
                xAxis.tickFormat(d => d > 1000 ? (d/1000).toFixed(0) + 'k'  : d);
            }
            if (i2 === 0) {
                if (CurQuery.length > 1 || this.ShowMode) {
                    svg
                        .append("g")
                        .attr("class", "xAxis")
                        .attr("transform", `translate(0, ${-20})`)
                        .call(xAxis)
                        .selectAll(".tick text")
                        .attr("dx", "0.5em")
                        .attr("dy", "-0.5em")
                        .attr('text-anchor', 'start')
                        .attr("transform", "rotate(-90)");
                    svg.select(".xAxis path").remove();
                } else {
                    svg
                        .append("g")
                        .attr("class", "xAxis")
                        .attr("transform", `translate(0, ${SvgHeight + 10})`)
                        .call(xAxis);
                    svg.select(".xAxis path").remove();
                }

                if (i1 === 0 && objectContainer.empty()) {
                    let yAxis;
                    if (CurQuery.length > 1 || this.ShowMode) {
                        yAxis = d3.axisLeft(xScale).tickValues(tickValues);
                    } else {
                        yAxis = d3.axisLeft(yScale);
                    }
                    svg
                        .append("g")
                        .attr("class", "yAxis")
                        .attr("transform", `translate(${-padding / 2}, 0)`)
                        .call(yAxis);
                    svg.select(".yAxis path").remove();
                }
            }

            // 非堆叠图
            // if (this.CurVisType === "histogram") {
            let rectContainer = container.filter((d) => typeof d[1] !== "object");
            if (!rectContainer.empty()) {
                let rectContainerG = rectContainer.append("g");
                rectContainerG
                    .append("rect")
                    .attr("x", ([category, value], i, a) => {
                        if (isNumericalX) {
                            let range = category.split("-").map((d) => Number(d));
                            return xScale(range[0]) + 5;
                        } else {
                            return xScale(category) + 5;
                        }
                    })
                    .attr("y", ([category, value]) => yScale(value))
                    .attr("width", ([category, value], i, a) => {
                        if (isNumericalX) {
                            let range = category.split("-").map((d) => Number(d));
                            return xScale(range[1]) - xScale(range[0]) - 10;
                        } else {
                            return bandwidth - 10;
                        }
                    })
                    .attr("height", ([category, value]) => {
                        if(this.noiseMode || !isSensitiveQuery) {
                            return Math.max(SvgHeight - 5 - yScale(value), 0)
                        } else {
                            return Math.max(SvgHeight - 5 - yScale(value -
                                this.getMultiNoise(1 / curEpsilon, noiseCount)), 0)
                        }
                    })
                    .attr("fill", this.BaseColorMap["grey-normal"])
                    .attr("fill-opacity", 0.5)
                    .attr("stroke", "none");
                if (this.noiseMode && (isSensitiveQuery || this.FilterSensitive)) {
                    rectContainerG
                        .append("line")
                        .attr("x1", (d, i, a) => {
                            let curBar = d3.select(a[i].previousSibling);
                            let x = +curBar.attr("x");
                            let width = +curBar.attr("width");
                            return x + width / 2;
                        })
                        .attr("x2", (d, i, a) => {
                            let curBar = d3.select(a[i]);
                            let x = +curBar.attr("x1");
                            return x;
                        })
                        .attr("y1", (d, i, a) => {
                            let curBar = d3.select(a[i].previousSibling);
                            let y = +curBar.attr("y");
                            return y + (yScale(0) - yScale(quartileNoise));
                        })
                        .attr("y2", (d, i, a) => {
                            let curBar = d3.select(a[i].previousSibling);
                            let y = +curBar.attr("y");
                            return y - (yScale(0) - yScale(quartileNoise));
                        })
                        .attr("stroke", this.BaseColorMap["grey-normal"])
                        .attr("stroke-width", "2px");
                    // 上线
                    rectContainerG
                        .append("line")
                        .attr("x1", (d, i, a) => {
                            let curBar = d3.select(a[i].previousSibling.previousSibling);
                            let x = +curBar.attr("x");
                            let width = +curBar.attr("width");
                            return x + width / 2 - width * 0.2;
                        })
                        .attr("x2", (d, i, a) => {
                            let curBar = d3.select(a[i].previousSibling.previousSibling);
                            let x = +curBar.attr("x");
                            let width = +curBar.attr("width");
                            return x + width / 2 + width * 0.2;
                        })
                        .attr("y1", (d, i, a) => {
                            let curBar = d3.select(a[i].previousSibling.previousSibling);
                            let y = +curBar.attr("y");
                            return y + (yScale(0) - yScale(quartileNoise));
                        })
                        .attr("y2", (d, i, a) => {
                            let curBar = d3.select(a[i].previousSibling.previousSibling);
                            let y = +curBar.attr("y");
                            return y + (yScale(0) - yScale(quartileNoise));
                        })
                        .attr("stroke", this.BaseColorMap["grey-normal"])
                        .attr("stroke-width", "2px");
                    //下线
                    rectContainerG
                        .append("line")
                        .attr("x1", (d, i, a) => {
                            let curBar = d3.select(
                                a[i].previousSibling.previousSibling.previousSibling
                            );
                            let x = +curBar.attr("x");
                            let width = +curBar.attr("width");
                            return x + width / 2 - 0.2 * width;
                        })
                        .attr("x2", (d, i, a) => {
                            let curBar = d3.select(
                                a[i].previousSibling.previousSibling.previousSibling
                            );
                            let x = +curBar.attr("x");
                            let width = +curBar.attr("width");
                            return x + width / 2 + 0.2 * width;
                        })
                        .attr("y1", (d, i, a) => {
                            let curBar = d3.select(
                                a[i].previousSibling.previousSibling.previousSibling
                            );
                            let y = +curBar.attr("y");
                            return y - (yScale(0) - yScale(quartileNoise));
                        })
                        .attr("y2", (d, i, a) => {
                            let curBar = d3.select(
                                a[i].previousSibling.previousSibling.previousSibling
                            );
                            let y = +curBar.attr("y");
                            return y - (yScale(0) - yScale(quartileNoise));
                        })
                        .attr("stroke", this.BaseColorMap["grey-normal"])
                        .attr("stroke-width", "2px");
                }
            }
            // rectContainerG
            //   .append("circle")
            //   .attr("cx", (d, i, a) => {
            //     let curBar = d3.select(a[i].previousSibling.previousSibling);
            //     let x = +curBar.attr("x");
            //     let width = +curBar.attr("width");
            //     return x + width / 2;
            //   })
            //   .attr("cy", (d, i, a) => {
            //     let curBar = d3.select(a[i].previousSibling.previousSibling);
            //     let y = +curBar.attr("y");
            //     return y;
            //   })
            //   .attr("r", 5);

            if (!objectContainer.empty()) {
                let isNumericalY = !this.AttrTypeMap[queryAttrs[1]] === '#' //isNaN(data[0][1][0][0].split("-")[0]);
                let yDomain = data[0][1].map(([category, value]) => category);
                let [yPosScale, yTickValues, yBandwidthScale, yBandwidth] =
                    this.GetScale(
                        isNumericalY,
                        yDomain,
                        [0, ticks2 * (RectWH + 5) + 5 + padding - RectWH * 0.6],
                        true
                    );
                if (i1 === 0) {
                    const yAxis = d3.axisLeft(yPosScale).tickValues(yTickValues);
                    svg
                        .append("g")
                        .attr("class", "yAxis")
                        .attr("transform", `translate(${-padding / 2}, 0)`)
                        .call(yAxis);
                    svg.select(".yAxis path").remove();
                }
                const colorScale = this.CurHeatMapColorScale;
                let minGranularityX;
                if (isNumericalX) {
                    minGranularityX =
                        this.AttrBinRangeMap[queryAttrs[0]][1] -
                        this.AttrBinRangeMap[queryAttrs[0]][0];
                }
                let minGranularityY;
                if (isNumericalY) {
                    minGranularityY =
                        this.AttrBinRangeMap[queryAttrs[1]][1] -
                        this.AttrBinRangeMap[queryAttrs[1]][0];
                }
                let xPn = 0;
                let yPn = 0;
                let innerG = objectContainer
                    .attr("bandwidth", ([category, value]) => {
                        let t = 1;
                        if (isNumericalX) {
                            let range = category.split("-").map((d) => Number(d));
                            t += Math.round((range[1] - range[0]) / minGranularityX) - 1;
                        }
                        return RectWH * t;
                    })
                    .attr("transform", ([category, value], i) => {
                        let xTrans;
                        xTrans = (i + xPn) * RectWH + 5 * (i + 1 + xPn);
                        if (isNumericalX) {
                            let range = category.split("-").map((d) => Number(d));
                            xPn += Math.round((range[1] - range[0]) / minGranularityX) - 1;
                        }
                        return `translate(${xTrans}, 0)`;
                    })
                    .selectAll(".innerG")
                    .data(
                        (d) => d[1],
                        (d) => d[0]
                    )
                    .join("g")
                    .attr("class", "innerG")
                    .attr("transform", ([category, value], i, a) => {
                        let yTrans;
                        yTrans = (i + yPn) * RectWH + 5 * (i + 1 + yPn);
                        if (isNumericalY) {
                            let range = category.split("-").map((d) => Number(d));
                            yPn += Math.round((range[1] - range[0]) / minGranularityY) - 1;
                        }
                        if (i == a.length - 1) {
                            yPn = 0;
                        }
                        return `translate(0, ${yTrans})`;
                    });

                innerG
                    .append("rect")
                    .attr("x", 0)
                    .attr("y", 0)
                    .attr("class", "queryResultRect")
                    .attr("width", ([category, value], i, a) => {
                        return d3.select(a[i].parentNode.parentNode).attr("bandwidth");
                    })
                    .attr("height", ([category, value], i, a) => {
                        let t = 1;
                        if (isNumericalY) {
                            let range = category.split("-").map((d) => Number(d));
                            t += Math.round((range[1] - range[0]) / minGranularityY) - 1;
                        }
                        return RectWH * t;
                    })
                    .attr("noiseCount", noiseCount)
                    .attr("stroke", this.BaseColorMap["white"])
                    .attr("stroke-width", "1px")
                    .attr("fill", ([category, value]) => {
                        if (this.noiseMode || !isSensitiveQuery) {
                            return colorScale(value);
                        } else {
                            return colorScale(
                                value -
                                this.getMultiNoise(1 / curEpsilon, noiseCount)
                            );
                        }
                    });
                if (this.noiseMode && (isSensitiveQuery || this.FilterSensitive)) {
                    innerG
                        .append("polygon")
                        .attr("class", ([category, value]) => `rect${category}`)
                        .attr("points", ([category, value], i, a) => {
                            let width = +d3
                                .select(a[i].parentNode.parentNode)
                                .attr("bandwidth");
                            let height = +d3.select(a[i].previousSibling).attr("height");
                            let noisePercent;
                            if (value !== 0) {
                                noisePercent = quartileNoise / value;
                                if (noisePercent > 0.8 || noisePercent < 0) noisePercent = 0.8;
                            } else {
                                noisePercent = 0.8;
                            }

                            let points = [
                                [0, 0],
                                [noisePercent * width, 0],
                                [0, height],
                            ];
                            return points.join(" ");
                        })
                        .attr("stroke", this.BaseColorMap["white"])
                        .attr("stroke-width", "1px")
                        .attr("fill", ([category, value]) =>
                            colorScale(value + quartileNoise)
                        );

                    innerG
                        .append("polygon")
                        .attr("class", ([category, value]) => `rect${category}`)
                        .attr("points", ([category, value], i, a) => {
                            let width = +d3
                                .select(a[i].parentNode.parentNode)
                                .attr("bandwidth");
                            let height = +d3
                                .select(a[i].previousSibling.previousSibling)
                                .attr("height");
                            let noisePercent;
                            if (value !== 0) {
                                noisePercent = quartileNoise / value;
                                if (noisePercent > 0.8 || noisePercent < 0) noisePercent = 0.8;
                            } else {
                                noisePercent = 0.8;
                            }
                            let points = [
                                [width, 0],
                                [width, height],
                                [width - noisePercent * width, height],
                            ];

                            return points.join(" ");
                        })
                        .attr("stroke", this.BaseColorMap["white"])
                        .attr("stroke-width", "1px")
                        .attr("fill", ([category, value]) =>
                            colorScale(value - quartileNoise)
                        );
                }
            }
        },
        showSummary() {
            let isFilter = this.isFilter;
            if (!this.ShowMode) {
                this.QueryConfirm(this.PreExeQuery)
                return;
            }
            if(isFilter === true) {
                let svg = d3.select("#QueryResultChart .content");
                svg.selectAll("*").remove();
                let padding = 200;
                svg
                    .append("rect")
                    .attr("x", padding * 0.7)
                    .attr("y", padding * 1.2)
                    .attr("width", this.SvgWidth - padding - 5)
                    .attr("height", this.SvgWidth - padding - 5)
                    .attr("fill", this.BaseColorMap["grey-deep"]);
                let TotalQueryAttrs = this.TotalQueryAttrs;
                let QueryAttrNamesLen = TotalQueryAttrs.length;
                let TotalQueryResults = this.TotalQueryResults;
                let ticksList = [];
                let totalTicks = TotalQueryAttrs.reduce((prev, cur) => {
                    let attrBinRange = this.AttrBinRangeMap[cur];
                    let ticks =
                        typeof attrBinRange[0] === "number"
                            ? attrBinRange.length - 1
                            : attrBinRange.length;
                    ticksList.push(ticks);
                    return prev + ticks;
                }, 0);

                let graphPadding = 10;
                let RectWH =
                    (this.SvgWidth - padding - QueryAttrNamesLen * graphPadding - 10) /
                    totalTicks -
                    5;
                let CurFilterAttr = this.CurFilterAttr;
                let queryAttrTupleList = [];
                for(let query of this.TotalQuerys) {
                    if(query.includes(CurFilterAttr)) {
                        for(let a1 of query) {
                            for(let a2 of query) {
                                if(a1 !== CurFilterAttr && a2 !== CurFilterAttr) {
                                    queryAttrTupleList.push([TotalQueryAttrs.indexOf(a1), TotalQueryAttrs.indexOf(a2)]);
                                }
                            }
                        }
                    }
                }
                // filter 数据
                let filterQueryRetMap = {};
                let PromiseList = [];
                TotalQueryAttrs.forEach((attr1, i1) => {
                    filterQueryRetMap[i1] = {};
                    TotalQueryAttrs.forEach((attr2, i2) => {
                        let QueryAttrs = i1 !== i2 ? [attr1, attr2] : [attr1];
                        if(queryAttrTupleList.findIndex(d => d[0]==i1&&d[1]==i2) !== -1) {
                            let QueryContent = this.CurQueryContent;
                            PromiseList.push(this.executeQuery(QueryAttrs, QueryContent));
                        }

                    })
                });
                let isFirst = false;
                Promise.all(PromiseList).then((data) => {
                    let tupleIdx = 0;
                    TotalQueryAttrs.forEach((attr1, i1) => {
                        TotalQueryAttrs.forEach((attr2, i2) => {
                            if(queryAttrTupleList.findIndex(d => d[0]==i1&&d[1]==i2) !== -1) {
                                let [queryRes, axisAttr] = data[tupleIdx];
                                filterQueryRetMap[i1][i2] = queryRes;
                                tupleIdx += 1;

                                if (i1 !== i2) {
                                    let epsilon = this.EpsilonMap[attr1][attr2];
                                    let noiseCount = this.NoiseCountMap[attr1][attr2];

                                    if(this.FilterSensitive || this.AttrSensitive[attr1] || this.AttrSensitive[attr2]) {
                                        for (let k1 in queryRes) {
                                            for (let k2 in queryRes[k1]) {
                                                queryRes[k1][k2] += this.getMultiNoise(
                                                    1 / epsilon,
                                                    noiseCount
                                                );
                                            }
                                        }
                                    }

                                    if (isFirst) {
                                        isFirst = false;
                                        const temp = Object.entries(queryRes);
                                        let maxVal = d3.max(temp, ([category, value]) =>
                                            typeof value === "object"
                                                ? d3.max(Object.entries(value), ([c, v]) => v)
                                                : value
                                        ) + this.calculateQuantile(
                                            0,
                                            1 / this.CurQueryEpsilonInput,
                                            0.475
                                        ) * (noiseCount+1);
                                        this.CurHeatMapColorScale = d3
                                            .scaleLinear()
                                            .domain([
                                                -maxVal,
                                                // -this.calculateQuantile(
                                                //     0,
                                                //     1 / epsilon,
                                                //     0.475
                                                // ) * (noiseCount+1) + Math.min(0, d3.min(temp, ([category, value]) =>
                                                //     typeof value === "object"
                                                //         ? d3.min(Object.entries(value), ([c, v]) => v)
                                                //         : value
                                                // )),
                                                0,
                                                maxVal,
                                            ])
                                            .range([
                                                this.BaseColorMap["red-sensitive"],
                                                this.BaseColorMap["white"],
                                                this.BaseColorMap["blue-normal"],
                                            ]);
                                    } else {
                                        const temp = Object.entries(queryRes);
                                        let scaleDomain = this.CurHeatMapColorScale.domain();
                                        let domainMax = scaleDomain[2];
                                        let nowMax = d3.max(temp, ([category, value]) =>
                                            typeof value === "object"
                                                ? d3.max(Object.entries(value), ([c, v]) => v)
                                                : value
                                        ) + this.calculateQuantile(
                                            0,
                                            1 / this.CurQueryEpsilonInput,
                                            0.475
                                        ) * (noiseCount+1);
                                        scaleDomain[2] = Math.max(domainMax, nowMax);
                                        let domainMin = scaleDomain[0];
                                        let nowMin = -nowMax;
                                        scaleDomain[0] = Math.min(domainMin, nowMin);
                                        this.CurHeatMapColorScale.domain(scaleDomain);
                                    }
                                }

                            }
                        })
                    });


                    // 绘图
                    TotalQueryAttrs.forEach((attr1, i1) => {
                        let transformX = 0;
                        for (let i = 0; i < i1; i++) {
                            transformX += ticksList[i];
                        }
                        TotalQueryAttrs.forEach((attr2, i2) => {
                            let transformY = 0;
                            for (let i = 0; i < i2; i++) {
                                transformY += ticksList[i];
                            }
                            // 绘制 attr title
                            if (i1 <= i2) {
                                svg
                                    .append("text")
                                    .attr(
                                        "x",
                                        padding +
                                        transformX * (RectWH + 5) +
                                        (ticksList[i1] * (RectWH + 5)) / 2 +
                                        10 -
                                        40 -
                                        20
                                    )
                                    .attr("y", 170)
                                    .attr("text-anchor", "middle")
                                    .classed('svg_sensitive_attr', this.AttrSensitive[attr1])
                                    .classed('svg_Nonsensitive_attr', !this.AttrSensitive[attr1])
                                    .text(attr1);
                                svg
                                    .append("text")
                                    .attr("x", 120)
                                    .attr(
                                        "y",
                                        padding * 1.2 +
                                        (RectWH + 5) * (transformY + ticksList[i2] / 2) -
                                        20
                                    )
                                    .attr("text-anchor", "middle")
                                    .attr(
                                        "transform",
                                        `rotate(-90 120 ${
                                            padding * 1.2 +
                                            (RectWH + 5) * (transformY + ticksList[i2] / 2) +
                                            30
                                        })`
                                    )
                                    .classed('svg_sensitive_attr', this.AttrSensitive[attr2])
                                    .classed('svg_Nonsensitive_attr', !this.AttrSensitive[attr2])
                                    .text(attr2);
                            }
                            // let [attr1, attr2] = [TotalQueryAttrs[i1], TotalQueryAttrs[i2]];

                            let QueryAttrs = i1 === i2 ? [attr1] : [attr1, attr2];
                            let chartContainer = svg
                                .append("g")
                                .attr(
                                    "transform",
                                    `translate(${
                                        i1 * graphPadding +
                                        0.7 * padding +
                                        (RectWH + 5) * transformX +
                                        5
                                    }, ${
                                        padding * 1.2 +
                                        i2 * graphPadding +
                                        (RectWH + 5) * transformY +
                                        5
                                    })`
                                )
                                .attr("id", `${attr1}±${attr2}`);
                            if(queryAttrTupleList.findIndex(d => d[0]==i1&&d[1]==i2) !== -1) {
                                let queryRes = filterQueryRetMap[i1][i2];


                                this.drawQueryResult(
                                    queryRes,
                                    QueryAttrs,
                                    chartContainer,
                                    [i1, i2],
                                    20,
                                    RectWH,
                                    [ticksList[i1], ticksList[i2]],
                                    this.NoiseCountMap[attr1][attr2],
                                    this.EpsilonMap[attr1][attr2]
                                );
                            }
                            else {
                                // 绘制 x 轴和 y 轴
                                if(i2===0) {
                                    let ticks1 = ticksList[i1];
                                    let isNumericalX = this.AttrTypeMap[attr1] == '#';
                                    let attr1Data = TotalQueryResults[attr1];
                                    let xDomain = Object.keys(attr1Data[Object.keys(attr1Data)[0]][0])
                                    let [xScale, tickValues, bandwidthScale, bandwidth] = this.GetScale(
                                        isNumericalX,
                                        xDomain,
                                        [0, ticks1 * (RectWH + 5) + 5],
                                        true
                                    );
                                    const xAxis = d3.axisBottom(xScale).tickValues(tickValues);
                                    chartContainer
                                        .append("g")
                                        .attr("class", "xAxis")
                                        .attr("transform", `translate(0, ${-20})`)
                                        .call(xAxis)
                                        .selectAll(".tick text")
                                        .attr("dx", "2em")
                                        .attr("dy", "-0.5em")
                                        .attr("transform", "rotate(-90)");
                                    chartContainer.select(".xAxis path").remove();
                                }
                                if(i1==0) {
                                    let isNumericalY = this.AttrTypeMap[attr2] == '#';
                                    let attr2Data = TotalQueryResults[attr2];
                                    let yDomain = Object.keys(attr2Data[Object.keys(attr2Data)[0]][0])
                                    let ticks2 = ticksList[i2];
                                    let padding = 20;
                                    let [yPosScale, yTickValues, yBandwidthScale, yBandwidth] =
                                        this.GetScale(
                                            isNumericalY,
                                            yDomain,
                                            [0, ticks2 * (RectWH + 5) + 5 + padding - RectWH * 0.6],
                                            true
                                        );
                                    const yAxis = d3.axisLeft(yPosScale).tickValues(yTickValues);
                                    chartContainer
                                        .append("g")
                                        .attr("class", "yAxis")
                                        .attr("transform", `translate(${-padding / 2}, 0)`)
                                        .call(yAxis);
                                    chartContainer.select(".yAxis path").remove();
                                }
                            }
                        })
                    })
                })


            }
            else {
                let svg = d3.select("#QueryResultChart .content");
                svg.selectAll("*").remove();
                let padding = 200;
                svg
                    .append("rect")
                    .attr("x", padding * 0.7)
                    .attr("y", padding * 1.2)
                    .attr("width", this.SvgWidth - padding - 5)
                    .attr("height", this.SvgWidth - padding - 5)
                    .attr("fill", this.BaseColorMap["grey-deep"]);
                let TotalQueryAttrs = this.TotalQueryAttrs.filter((d) => d !== this.CurFilterAttr);
                let QueryAttrNamesLen = TotalQueryAttrs.length;
                let TotalQueryResults = this.TotalQueryResults;
                let ticksList = [];
                let totalTicks = TotalQueryAttrs.reduce((prev, cur) => {
                    let attrBinRange = this.AttrBinRangeMap[cur];
                    let ticks =
                        typeof attrBinRange[0] === "number"
                            ? attrBinRange.length - 1
                            : attrBinRange.length;
                    ticksList.push(ticks);
                    return prev + ticks;
                }, 0);

                let graphPadding = 10;
                let RectWH =
                    (this.SvgWidth - padding - QueryAttrNamesLen * graphPadding - 10) /
                    totalTicks -
                    5;

                // 统一颜色比例尺
                let isFirst = true;
                TotalQueryAttrs.forEach((attr1, i1) => {
                    TotalQueryAttrs.forEach((attr2, i2) => {
                        if (i1 !== i2 && TotalQueryResults[attr1][attr2]) {
                            let queryRes = TotalQueryResults[attr1][attr2][0];
                            let noiseCount = this.NoiseCountMap[attr1][attr2];
                            let epsilon = this.EpsilonMap[attr1][attr2];
                            if (isFirst) {
                                isFirst = false;
                                const temp = Object.entries(queryRes);
                                let maxVal = d3.max(temp, ([category, value]) =>
                                    typeof value === "object"
                                        ? d3.max(Object.entries(value), ([c, v]) => v)
                                        : value
                                ) + this.calculateQuantile(
                                    0,
                                    1 / epsilon,
                                    0.475
                                ) * (noiseCount+1);
                                this.CurHeatMapColorScale = d3
                                    .scaleLinear()
                                    .domain([
                                        -maxVal,
                                        0,
                                        maxVal,
                                    ])
                                    .range([
                                        this.BaseColorMap["orange"],
                                        this.BaseColorMap["white"],
                                        this.BaseColorMap["green"],
                                    ]);
                            } else {
                                const temp = Object.entries(queryRes);
                                let scaleDomain = this.CurHeatMapColorScale.domain();
                                let domainMax = scaleDomain[2];
                                let nowMax = d3.max(temp, ([category, value]) =>
                                    typeof value === "object"
                                        ? d3.max(Object.entries(value), ([c, v]) => v)
                                        : value
                                ) + this.calculateQuantile(
                                    0,
                                    1 / epsilon,
                                    0.475
                                ) * (noiseCount+1);
                                scaleDomain[2] = Math.max(domainMax, nowMax);
                                let domainMin = scaleDomain[0];
                                let nowMin = -nowMax;
                                scaleDomain[0] = Math.min(domainMin, nowMin);
                                this.CurHeatMapColorScale.domain(scaleDomain);
                            }
                        }
                    })
                })

                TotalQueryAttrs.forEach((attr1, i1) => {
                    let transformX = 0;
                    for (let i = 0; i < i1; i++) {
                        transformX += ticksList[i];
                    }
                    TotalQueryAttrs.forEach((attr2, i2) => {
                        let transformY = 0;
                        for (let i = 0; i < i2; i++) {
                            transformY += ticksList[i];
                        }

                        let QueryAttrs = i1 === i2 ? [attr1] : [attr1, attr2];
                        let chartContainer = svg
                            .append("g")
                            .attr(
                                "transform",
                                `translate(${
                                    i1 * graphPadding +
                                    0.7 * padding +
                                    (RectWH + 5) * transformX +
                                    5
                                }, ${
                                    padding * 1.2 +
                                    i2 * graphPadding +
                                    (RectWH + 5) * transformY +
                                    5
                                })`
                            )
                            .attr("id", `${attr1}±${attr2}`);
                        if (i1 <= i2) {
                            svg
                                .append("text")
                                .attr(
                                    "x",
                                    padding +
                                    transformX * (RectWH + 5) +
                                    (ticksList[i1] * (RectWH + 5)) / 2 +
                                    10 -
                                    40 -
                                    20
                                )
                                .attr("y", 170)
                                .attr("text-anchor", "middle")
                                .classed('svg_sensitive_attr', this.AttrSensitive[attr1])
                                .classed('svg_Nonsensitive_attr', !this.AttrSensitive[attr1])
                                .text(attr1);
                            svg
                                .append("text")
                                .attr("x", 120)
                                .attr(
                                    "y",
                                    padding * 1.2 +
                                    (RectWH + 5) * (transformY + ticksList[i2] / 2) -
                                    20
                                )
                                .attr("text-anchor", "middle")
                                .attr(
                                    "transform",
                                    `rotate(-90 120 ${
                                        padding * 1.2 +
                                        (RectWH + 5) * (transformY + ticksList[i2] / 2) +
                                        30
                                    })`
                                )
                                .classed('svg_sensitive_attr', this.AttrSensitive[attr2])
                                .classed('svg_Nonsensitive_attr', !this.AttrSensitive[attr2])
                                .text(attr2);
                        }
                        if (TotalQueryResults[attr1][attr2]) {
                            let [queryRes, axisAttr] = TotalQueryResults[attr1][attr2];

                            this.drawQueryResult(
                                queryRes,
                                QueryAttrs,
                                chartContainer,
                                [i1, i2],
                                20,
                                RectWH,
                                [ticksList[i1], ticksList[i2]],
                                this.NoiseCountMap[attr1][attr2],
                                this.EpsilonMap[attr1][attr2]
                            );
                        }
                        else {
                            // 绘制 x 轴和 y 轴
                            if(i2===0) {
                                let ticks1 = ticksList[i1];
                                let isNumericalX = this.AttrTypeMap[attr1] == '#';
                                let attr1Data = TotalQueryResults[attr1];
                                let xDomain = Object.keys(attr1Data[Object.keys(attr1Data)[0]][0])
                                let [xScale, tickValues, bandwidthScale, bandwidth] = this.GetScale(
                                    isNumericalX,
                                    xDomain,
                                    [0, ticks1 * (RectWH + 5) + 5],
                                    true
                                );
                                const xAxis = d3.axisBottom(xScale).tickValues(tickValues);
                                chartContainer
                                    .append("g")
                                    .attr("class", "xAxis")
                                    .attr("transform", `translate(0, ${-20})`)
                                    .call(xAxis)
                                    .selectAll(".tick text")
                                    .attr("dx", "2em")
                                    .attr("dy", "-0.5em")
                                    .attr("transform", "rotate(-90)");
                                chartContainer.select(".xAxis path").remove();
                            }
                            if(i1==0) {
                                let isNumericalY = this.AttrTypeMap[attr2] == '#';
                                let attr2Data = TotalQueryResults[attr2];
                                let yDomain = Object.keys(attr2Data[Object.keys(attr2Data)[0]][0])
                                let ticks2 = ticksList[i2];
                                let padding = 20;
                                let [yPosScale, yTickValues, yBandwidthScale, yBandwidth] =
                                    this.GetScale(
                                        isNumericalY,
                                        yDomain,
                                        [0, ticks2 * (RectWH + 5) + 5 + padding - RectWH * 0.6],
                                        true
                                    );
                                const yAxis = d3.axisLeft(yPosScale).tickValues(yTickValues);
                                chartContainer
                                    .append("g")
                                    .attr("class", "yAxis")
                                    .attr("transform", `translate(${-padding / 2}, 0)`)
                                    .call(yAxis);
                                chartContainer.select(".yAxis path").remove();
                            }
                        }
                    });
                });
            }

        },

        // 事件类函数
        handleEPSliderChange(newVal) {
            if (newVal < this.OldExplorationProgressVal) {
                this.ExplorationProgressVal = this.OldExplorationProgressVal;
                console.log(this.ExplorationProgressVal)
                // this.$message('滑块值只能增加，不能减少！');
                // this.$refs.slider.setValue(this.OldExplorationProgressVal); // 假设你有一个对slider的引用
            } else {
                this.OldExplorationProgressVal = newVal;
                console.log(this.ExplorationProgressVal)
            }
        },
        showAttrBin(attr, bin) {
            this.AttrBinRangeShowMap[attr][bin] = true;
        },
        hiddenAttrBin(attr, bin) {
            this.AttrBinRangeShowMap[attr][bin] = false;
        },
        reverseQueryBin(cna, bin) {
            let aqbr = this.AttrQueryBinRangeMap[cna];
            console.log("xxx");
            if (aqbr.includes(bin)) {
                aqbr.splice(aqbr.indexOf(bin), 1);
            } else {
                aqbr.push(bin);
                aqbr.sort((a, b) => a - b);
                console.log(aqbr);
            }
        },
        ConfirmAddAttr() {
            if (this.TempAttr !== "") {
                this.CurExeQuery.push(this.TempAttr);
            }
            this.AddState = false;
            this.TempAttr = "";
        },
        AddNewAttr() {
            this.AddState = true;
        },
        deleteExeAttr(attr) {
            this.CurExeQuery.splice(this.CurExeQuery.indexOf(attr), 1);
        },
        ResetHistogram() {
            let simulateData = {};
            let thisNodeName = this.CurThisNodeName;
            let VueThis = this;
            let binRange = VueThis.AttrBinRangeMap[thisNodeName];
            let baseVal = VueThis.CurExDataset.length / (binRange.length - 1);
            if (this.AttrTypeMap[thisNodeName] === "#") {
                for (let i in binRange) {
                    let idx = +i;
                    if (idx !== 0) {
                        let noise = (Math.random() * baseVal) / 2;
                        simulateData[binRange[idx - 1] + "-" + binRange[idx]] =
                            baseVal + noise;
                    }
                }
            } else {
                for (let v of binRange) {
                    let noise = (Math.random() * baseVal) / 2;
                    simulateData[v] = baseVal + noise;
                }
            }
            VueThis.simulateDataRecord[thisNodeName] = simulateData;
            VueThis.SensitiveAttrSimulate[thisNodeName] = simulateData;
            VueThis.updateAttrHistogram(thisNodeName, simulateData);
            VueThis.updateSimulatedAttrLineChart(thisNodeName, simulateData);
        },
        editText(lineName, coorelation) {
            this.CurInputText = coorelation;
            this.CurLineName = lineName;
            if (this.CorrQueryMap[lineName] === undefined) {
                this.CorrQueryMap[lineName] = "";
            }
            this.ShowCorrInput = true;
        },
        confirmText() {
            // 更新文本并关闭输入框
            this.CorrQueryMap[this.CurLineName] = this.CurInputText;
            this.ShowCorrInput = false;
            d3.select(`#${this.CurLineName}text`).text(parseFloat(this.CurInputText));
            this.SimulatedCorrelationMap[this.CurLineName] = parseFloat(this.CurInputText);
            // console.log(this.AttrBinRangeMap[this.CurLineNonSensitiveAttr]);
            // axios({
            //   method: "post",
            //   url: "http://127.0.0.1:8000/Utils/SensitiveHistogram/",
            //   data: {
            //     correlate: parseFloat(this.CurInputText),
            //     nonSensitiveAttrList: this.CurExDataset.map(
            //       (d) => d[this.CurLineNonSensitiveAttr]
            //     ),
            //     nonSensitiveAttrBinRange:
            //       this.AttrBinRangeMap[this.CurLineNonSensitiveAttr],
            //     SensitiveHistogram:
            //       this.SensitiveAttrSimulate[this.CurLineSensitiveAttr],
            //   },
            // }).then((response) => {
            //   let data = response.data;
            //   console.log(data);
            // });
        },
        ResetHeatMap() {
            let colorScale = this.CurHeatMapColorScale;
            d3.selectAll(".queryResultRect").attr(
                "fill",
                ([category, value], i, a) => {
                    if (this.noiseMode) {
                        return colorScale(value);
                    } else {
                        let noiseCount = +d3.select(a[i]).attr("noiseCount");
                        return colorScale(
                            value -
                            this.getMultiNoise(1 / this.CurQueryEpsilonInput, noiseCount)
                        );
                    }
                }
            );
        },

        QueryConfirmWithEpsilon() {
            // this.isSimulation = false;
            this.TotalEpsilonMap[this.CurDatabase] -= this.CurQueryEpsilonInput;
            // this.StrategySpecific[this.CurQueryStrategyIdx]["QueryEpsilonList"][
            //   this.CurQueryIdx
            // ];
            this.TotalQueryAttrs = [
                ...new Set(this.TotalQueryAttrs.concat(this.CurQuery)),
            ];
            this.TotalQuerys.push(JSON.parse(JSON.stringify(this.CurQuery)));

            this.CurQueryList = this.CurQueryList.filter((d) => {
                console.log("this.CurQuery", this.CurQuery);
                return !(this.CurQuery.includes(d[0]) && this.CurQuery.includes(d[1]));
            });
            this.CurIssueState = true;
            this.QueryConfirm();
            this.CurSimulateState = false;
            this.CurQueryState = "for Feedback";
            this.CurQueryIdx = 0;
            this.CurQueryStrategyIdx = 0;
            // this.TotalEpsilonMap[this.CurDatabase] -= this.CurQueryEpsilon;

            this.PreQueryEpsilon = this.CurQueryEpsilonInput;
            // this.QueryHistory.push({
            //     queryAttr: this.CurQuery,
            //     epsilon: this.CurQueryEpsilon,
            // });
        },
        QueryIssue() {
            this.isSimulation = false;
            this.QueryConfirmWithEpsilon();
        },
        QuerySimulate() {
            this.isSimulation = true;
            this.QueryConfirm();
        },
        QueryConfirm(PreExeQuery, PreQueryEpsilon) {
            this.CurQueryState = "for Simulation";
            this.CurSimulateState = true;
            this.CurSimulateResult = {};
            let padding = 200;
            this.NoiseMap = this.getNoiseMap(0, 1);
            let svg = d3.select("#QueryResultChart .content");
            let epsilon;
            if(PreQueryEpsilon) {
                epsilon = PreQueryEpsilon;
            }
            else {
                epsilon = this.CurQueryEpsilonInput;
                if(epsilon === 0) epsilon = 2;
            }
            svg.selectAll("*").remove();
            svg
                .append("rect")
                .attr("x", padding * 0.7)
                .attr("y", padding * 1.2)
                .attr("width", this.SvgWidth - padding - 5)
                .attr("height", this.SvgWidth - padding - 5)
                .attr("fill", this.BaseColorMap["grey-deep"])
                .attr("fill-opacity", 0.3);
            let CurQuery
            if(Array.isArray(PreExeQuery)) {
                CurQuery = JSON.parse(JSON.stringify(PreExeQuery));
            } else {
                CurQuery = JSON.parse(JSON.stringify(this.CurExeQuery));
            }
            this.PreExeQuery = JSON.parse(JSON.stringify(CurQuery));
            CurQuery = CurQuery.filter((d) => d !== this.CurFilterAttr);
            if (CurQuery.length <= 1) {
                let ticksList = [];
                let SVGSize = [
                    this.SvgWidth - padding - 10,
                    this.SvgHeight - padding - 9,
                ];
                let totalTicks = CurQuery.reduce((prev, cur) => {
                    let attrBinRange = this.AttrBinRangeMap[cur];
                    let ticks =
                        typeof attrBinRange[0] === "number"
                            ? attrBinRange.length - 1
                            : attrBinRange.length;
                    ticksList.push(ticks);
                    return prev + ticks;
                }, 0);
                let RectWH = (this.SvgWidth - padding - 20) / totalTicks - 5;
                let yTickNum = Math.floor(SVGSize[0] / (RectWH+5));
                let QueryContent = this.CurQueryContent;
                this.executeQuery(CurQuery, QueryContent).then(
                    ([queryRes, axisAttr]) => {
                        const temp = Object.entries(queryRes);
                        this.CurHeatMapColorScale = d3
                            .scaleLinear()
                            .domain([
                                -this.calculateQuantile(
                                    0,
                                    1 / epsilon,
                                    0.475
                                ),
                                0,
                                d3.max(temp, ([category, value]) =>
                                    typeof value === "object"
                                        ? d3.max(Object.entries(value), ([c, v]) => v)
                                        : value
                                ),
                            ])
                            .range([
                                this.BaseColorMap["orange"],
                                this.BaseColorMap["white"],
                                this.BaseColorMap["green"],
                            ]);
                        let graphPadding = 10;
                        let chartContainer = svg
                            .append("g")
                            .attr(
                                "transform",
                                `translate(${0.7 * padding + 5}, ${padding * 1.2 + 5})`
                            )
                            .attr("id", `${CurQuery[0]}±${CurQuery[1]}`);

                        svg
                            .append("text")
                            .attr(
                                "x",
                                padding + (ticksList[0] * (RectWH + 5)) / 2 + 10 - 40 - 20
                            )
                            .attr("y", 1010)
                            .attr("text-anchor", "middle")
                            .text(CurQuery[0]);
                        let attrList = CurQuery;
                        let noiseCount = this.PreExeQuery.reduce((pre, cur) => {
                            if (attrList.includes(cur)) {
                                return pre;
                            } else {
                                let sub = this.AttrTypeMap[cur] == "#" ? 1 : 0;
                                return pre * (this.AttrQueryBinRangeMap[cur].length - sub);
                            }
                        }, 1);


                        this.QueryConfirmMeta(
                            CurQuery,
                            chartContainer,
                            [queryRes, axisAttr],
                            SVGSize,
                            [0, 0],
                            20,
                            RectWH,
                            [ticksList[0], yTickNum],
                            noiseCount,
                            epsilon
                        );
                    }
                );
            }
            // 多属性的情况
            else {
                let QueryAttrNames = CurQuery;
                let QueryAttrNamesLen = QueryAttrNames.length;

                let SVGSize = [
                    (this.SvgWidth - padding) / QueryAttrNamesLen,
                    (this.SvgHeight - padding) / QueryAttrNamesLen,
                ];
                let ticksList = [];
                let totalTicks = QueryAttrNames.reduce((prev, cur) => {
                    let attrBinRange = this.AttrBinRangeMap[cur];
                    let ticks =
                        typeof attrBinRange[0] === "number"
                            ? attrBinRange.length - 1
                            : attrBinRange.length;
                    ticksList.push(ticks);
                    return prev + ticks;
                }, 0);
                let graphPadding = 10;
                let RectWH =
                    (this.SvgWidth - padding - QueryAttrNamesLen * graphPadding - 10) /
                    totalTicks -
                    5;
                let isFirst = true;
                let queryRetMap = {};
                let PromiseList = [];

                // 模拟的情况，需要先获得多属性联合分布，然后转化为双属性分布结果
                if (this.isSimulation) {
                    let CoorelationMatrix = [];
                    for (let i in CurQuery) {
                        CoorelationMatrix.push([]);
                        for (let j in CurQuery) {
                            if (i != j) {
                                let a1 = CurQuery[+i];
                                let a2 = CurQuery[+j];
                                let NodeNameList = [a1, a2].sort();
                                let lineName = `${NodeNameList[0]}±${NodeNameList[1]}`;
                                CoorelationMatrix[i].push(
                                    +this.SimulatedCorrelationMap[lineName]
                                );
                            } else {
                                CoorelationMatrix[i].push(1);
                            }
                        }
                    }
                    PromiseList.push(
                        new Promise((resolve) => {
                            axios({
                                method: "post",
                                url: "http://127.0.0.1:8000/Utils/CorrelatedHistogram/",
                                data: {
                                    correlate: CoorelationMatrix, //parseFloat(this.CurInputText),
                                    QueryResList: CurQuery.map(
                                        (d) => this.simulateDataRecord[d]
                                    ),
                                    QueryBinRangeList: CurQuery.map(
                                        (d) => this.AttrQueryBinRangeMap[d]
                                    ),
                                    'AttrTypeList': CurQuery.map(d => this.AttrTypeMap[d]),
                                    size: this.CurExDataset.length,
                                },
                            }).then((response) => {
                                let data = response.data;
                                resolve(data.ret);
                            });
                        })
                    );
                } else {
                    QueryAttrNames.forEach((attr1, i1) => {
                        let transformX = 0;
                        for (let i = 0; i < i1; i++) {
                            transformX += ticksList[i];
                        }
                        queryRetMap[i1] = {};
                        QueryAttrNames.forEach((attr2, i2) => {
                            // if(i1 >= i2) {
                                let QueryAttrs = i1 !== i2 ? [attr1, attr2] : [attr1];
                                let QueryContent = this.CurQueryContent;
                                PromiseList.push(this.executeQuery(QueryAttrs, QueryContent));
                            // }
                        });
                    });
                }
                let QueryAttrNum = CurQuery.length;
                Promise.all(PromiseList).then((data) => {
                    if (data.length == 1) {
                        data = data[0];
                    }
                    let Idx = 0;
                    let noiseCount;
                    let layer = 0;
                    for (let [queryRes, axisAttr] of data) {

                        let i1 = Math.floor(Idx / QueryAttrNum);//Idx//
                        let i2 = Idx % QueryAttrNum;
                        // if(Idx===QueryAttrNum-1) {
                        //     layer += 1;
                        //     Idx = layer-1;
                        // }
                        Idx += 1;
                        if (queryRetMap[i1] === undefined) queryRetMap[i1] = {};
                        queryRetMap[i1][i2] = [queryRes, axisAttr];
                        let attrList = [
                            ...new Set([CurQuery[i1], CurQuery[i2]]),
                        ];
                        noiseCount = this.PreExeQuery.reduce((pre, cur) => {
                            if (attrList.includes(cur)) {
                                return pre;
                            } else {
                                let sub = this.AttrTypeMap[cur] == "#" ? 1 : 0;
                                return pre * (this.AttrQueryBinRangeMap[cur].length - sub);
                            }
                        }, 1);

                        // simulate 和 issue 的情况都需要考虑噪声累加
                        // if(!this.isSimulation) {
                        if(this.FilterSensitive || this.AttrSensitive[CurQuery[i1]] || this.AttrSensitive[CurQuery[i2]]) {
                            if (i1 != i2) {
                                for (let k1 in queryRes) {
                                    for (let k2 in queryRes[k1]) {
                                        queryRes[k1][k2] += this.getMultiNoise(
                                            1 / epsilon,
                                            noiseCount
                                        );
                                    }
                                }
                            } else {
                                for (let k in queryRes) {
                                    queryRes[k] += this.getMultiNoise(
                                        1 / epsilon,
                                        noiseCount
                                    );
                                }
                            }
                        }
                        // }

                        if (i1 !== i2) {
                            // let epsilon = this.CurQueryEpsilonInput;
                            if(!this.isSensitiveQuery(CurQuery) && !this.FilterSensitive) {
                                epsilon = 0.1;
                                noiseCount = -1;
                            }
                            if (isFirst) {
                                isFirst = false;
                                const temp = Object.entries(queryRes);
                                let maxVal = d3.max(temp, ([category, value]) =>
                                    typeof value === "object"
                                        ? d3.max(Object.entries(value), ([c, v]) => v)
                                        : value
                                ) + this.calculateQuantile(
                                    0,
                                    1 / epsilon,
                                    0.475
                                ) * (noiseCount+1);
                                    this.CurHeatMapColorScale = d3
                                    .scaleLinear()
                                    .domain([
                                        -maxVal,
                                        0,
                                        maxVal,
                                    ])
                                    .range([
                                        this.BaseColorMap["orange"],
                                        this.BaseColorMap["white"],
                                        this.BaseColorMap["green"],
                                    ]);
                            } else {
                                const temp = Object.entries(queryRes);
                                let scaleDomain = this.CurHeatMapColorScale.domain();
                                let domainMax = scaleDomain[2];
                                let nowMax = d3.max(temp, ([category, value]) =>
                                    typeof value === "object"
                                        ? d3.max(Object.entries(value), ([c, v]) => v)
                                        : value
                                ) + this.calculateQuantile(
                                    0,
                                    1 / epsilon,
                                    0.475
                                ) * (noiseCount+1);
                                scaleDomain[2] = Math.max(domainMax, nowMax);
                                let domainMin = scaleDomain[0];
                                let nowMin = -nowMax;
                                scaleDomain[0] = Math.min(domainMin, nowMin);
                                this.CurHeatMapColorScale.domain(scaleDomain);
                            }
                        }
                    }
                    QueryAttrNames.forEach((attr1, i1) => {
                        let transformX = 0;
                        for (let i = 0; i < i1; i++) {
                            transformX += ticksList[i];
                        }
                        QueryAttrNames.forEach((attr2, i2) => {
                            let transformY = 0;
                            for (let i = 0; i < i2; i++) {
                                transformY += ticksList[i];
                            }
                            // element 和 nextElement 分别为数组中的两个元素

                            let QueryAttrs = i1 === i2 ? [attr1] : [attr1, attr2];
                            let chartContainer = svg
                                .append("g")
                                .attr(
                                    "transform",
                                    `translate(${
                                        i1 * graphPadding +
                                        0.7 * padding +
                                        (RectWH + 5) * transformX +
                                        5
                                    }, ${
                                        padding * 1.2 +
                                        i2 * graphPadding +
                                        (RectWH + 5) * transformY +
                                        5
                                    })`
                                )
                                .attr("id", `${attr1}±${attr2}`);
                            if (i1 <= i2) {
                                svg
                                    .append("text")
                                    .attr(
                                        "x",
                                        padding +
                                        transformX * (RectWH + 5) +
                                        (ticksList[i1] * (RectWH + 5)) / 2 +
                                        10 -
                                        40 -
                                        20
                                    )
                                    .attr("y", 170)
                                    .attr("text-anchor", "middle")
                                    .classed('svg_sensitive_attr', this.AttrSensitive[attr1])
                                    .classed('svg_Nonsensitive_attr', !this.AttrSensitive[attr1])
                                    .text(attr1)
                                svg
                                    .append("text")
                                    .attr("x", 120)
                                    .attr(
                                        "y",
                                        padding * 1.2 +
                                        (RectWH + 5) * (transformY + ticksList[i2] / 2) -
                                        20
                                    )
                                    .attr("text-anchor", "middle")
                                    .attr(
                                        "transform",
                                        `rotate(-90 120 ${
                                            padding * 1.2 +
                                            (RectWH + 5) * (transformY + ticksList[i2] / 2) +
                                            30
                                        })`
                                    )
                                    .classed('svg_sensitive_attr', this.AttrSensitive[attr2])
                                    .classed('svg_Nonsensitive_attr', !this.AttrSensitive[attr2])
                                    .text(attr2);
                            }

                            // if(i1 < i2) {
                            //     [i1, i2] = [i2, i1]
                            // }
                            let [queryRes, axisAttr] = queryRetMap[i1][i2];
                            if (this.NoiseCountMap[attr1] === undefined) {
                                this.NoiseCountMap[attr1] = {};
                            }
                            this.NoiseCountMap[attr1][attr2] = noiseCount;
                            if (this.EpsilonMap[attr1] === undefined) {
                                this.EpsilonMap[attr1] = {};
                            }
                            this.EpsilonMap[attr1][attr2] = epsilon; //this.CurQueryEpsilonInput;
                            this.QueryConfirmMeta(
                                QueryAttrs,
                                chartContainer,
                                [queryRes, axisAttr],
                                SVGSize,
                                [i1, i2],
                                20,
                                RectWH,
                                [ticksList[i1], ticksList[i2]],
                                noiseCount,
                                epsilon
                            );
                        });
                    });
                    // this.isSimulation = true;
                });
            }
        },
        QueryConfirmMeta(
            QueryAttrs,
            chartContainer,
            [queryRes, axisAttr],
            SVGSize,
            [i1, i2],
            padding,
            RectWH,
            [ticks1, ticks2],
            noiseCount,
            epsilon
        ) {
            // 将敏感属性的查询结果转化为分布结果
            // 必定是双属性/单属性
            let data = {};
            if (!this.isSimulation) {
                if (this.TotalQueryResults[QueryAttrs[0]] === undefined) {
                    this.TotalQueryResults[QueryAttrs[0]] = {};
                }
                if (QueryAttrs.length > 1) {
                    this.TotalQueryResults[QueryAttrs[0]][QueryAttrs[1]] = [queryRes];
                } else {
                    this.TotalQueryResults[QueryAttrs[0]][QueryAttrs[0]] = [queryRes];
                }
                if (QueryAttrs.length > 1) {
                    if (this.AttrSensitive[QueryAttrs[0]]) {
                        data = JSON.parse(JSON.stringify(queryRes));
                        for (let key in data) {
                            if (typeof data[key] === "number") break;
                            if(Object.values(data[key]).length == 0) {
                                data[key] = 0;
                                continue;
                            }
                            data[key] = Object.values(data[key]).reduce(function (
                                prev,
                                curr,
                                idx,
                                arr
                            ) {
                                return prev + curr;
                            });
                        }
                        this.VerifiedDataRecord[QueryAttrs[0]] = data;
                        this.updateVerifiedAttrLineChart(QueryAttrs[0], data);
                        this.updateSimulatedAttrLineChart(
                            QueryAttrs[0],
                            this.simulateDataRecord[QueryAttrs[0]]
                        );
                        console.log(data, this.simulateDataRecord[QueryAttrs[0]]);
                    } else if(this.AttrSensitive[QueryAttrs[1]]){
                        for (let key in queryRes) {
                            let dks = Object.keys(queryRes[key]);
                            for (let dk of dks) {
                                data[dk] = data[dk] ? data[dk] : 0;
                                data[dk] += queryRes[key][dk];
                            }
                        }
                        this.VerifiedDataRecord[QueryAttrs[1]] = data;
                        this.updateVerifiedAttrLineChart(QueryAttrs[1], data);
                        this.updateSimulatedAttrLineChart(
                            QueryAttrs[1],
                            this.simulateDataRecord[QueryAttrs[1]]
                        );
                        console.log(data, this.simulateDataRecord[QueryAttrs[1]]);
                    }
                }
            }

            // 绘制查询结果
            this.drawQueryResult(
                queryRes,
                QueryAttrs,
                chartContainer,
                [i1, i2],
                padding,
                RectWH,
                [ticks1, ticks2],
                noiseCount,
                epsilon
            );
        },
        // AddBreakPoint(attr) {
        //   let sliderList = this.AttrBinRangeMap[attr];
        //   let copyList = Array.from(sliderList);
        //   copyList.splice(1, 0, (sliderList[0] + sliderList[1]) / 2);
        //   this.AttrBinRangeMap[attr] = copyList;
        //   console.log(this.AttrBinRangeMap[attr]);
        // },
        ConfirmQueryTemplate() {
            this.QueryConfirm();
        },
        chooseCurQuery(strategyI, queryI) {
            this.CurQueryStrategyIdx = strategyI;
            this.CurQueryIdx = queryI;
            this.CurQueryEpsilonInput =
                this.StrategySpecific[this.CurQueryStrategyIdx]["QueryEpsilonList"][
                    this.CurQueryIdx
                    ];

            // 修改 this.AttrQueryBinRangeMap
            let granularity =
                this.StrategySpecific[strategyI]["QueryGranularity"][queryI];
            // for (let i in this.CurExeQuery) {
            //
            //     if (granularity[i] === 2) {
            //         this.AttrQueryBinRangeMap[this.CurExeQuery[+i]] = this.AttrQueryBinRangeMap[this.CurExeQuery[+i]].filter(
            //             (d, i) => i % 2 === 0
            //         );
            //     } else if (granularity[i] === 4){
            //         this.AttrQueryBinRangeMap[this.CurExeQuery[+i]] = this.AttrQueryBinRangeMap[this.CurExeQuery[+i]].filter(
            //             (d, i) => i % 4 === 0 || i % 4 === 3
            //         );
            //     }
            // }
        },

        // 细节类函数
        GetScale(isNumerical, domain, range, isFilledDomain) {
            let scale, tickValues, bandwidthScale, bandwidth;
            if (isNumerical) {
                // 数值型
                let finalDomain = domain[domain.length - 1].split("-");
                let numericalDomain;
                if (isFilledDomain) {
                    numericalDomain = [Number(domain[0].split("-")[0]), +finalDomain[1]];
                } else {
                    numericalDomain = [
                        Number(domain[0].split("-")[0]),
                        +finalDomain[1] + (+finalDomain[1] - +finalDomain[0]) * 0.3,
                    ];
                }
                scale = d3.scaleLinear().domain(numericalDomain).range(range);
                tickValues = domain.map((d) => Number(d.split("-")[0]));
                tickValues.push(Number(domain[domain.length - 1].split("-")[1]));
                bandwidthScale =
                    (range[1] - range[0]) / (domain[domain.length - 1] - domain[0]);
            } else {
                // 类别型
                scale = d3.scaleBand().domain(domain).range(range);
                tickValues = scale.domain();
                bandwidth = scale.bandwidth();
            }
            return [scale, tickValues, bandwidthScale, bandwidth];
        },
        // 双属性查询
        executeDbAttrQuery(QueryAttrs, QueryContent, isSimulation) {
            let is;
            if(isSimulation) {
                is=isSimulation
            } else {
                is = this.isSimulation;
            }
            let QueryAttrNames = [QueryAttrs[0], QueryAttrs[1]];
            if (
                is &&
                (this.AttrSensitive[QueryAttrs[0]] || this.AttrSensitive[QueryAttrs[1]])
            ) {
                let a1 = QueryAttrs[0];
                let a2 = QueryAttrs[1];
                let s1 = this.AttrSensitive[a1];
                let s2 = this.AttrSensitive[a2];
                let NodeNameList = [a1, a2].sort();
                let lineName = `${NodeNameList[0]}±${NodeNameList[1]}`;
                let coorelation = +this.SimulatedCorrelationMap[lineName];
                return new Promise((resolve) => {
                    axios({
                        method: "post",
                        url: "http://127.0.0.1:8000/Utils/CorrelatedHistogram/",
                        data: {
                            correlate: [
                                [1, coorelation],
                                [coorelation, 1],
                            ], //parseFloat(this.CurInputText),
                            QueryResList: [
                                this.simulateDataRecord[a1],
                                this.simulateDataRecord[a2],
                            ],
                            QueryBinRangeList: [
                                this.AttrQueryBinRangeMap[a1],
                                this.AttrQueryBinRangeMap[a2],
                            ],
                            'AttrTypeList': [a1, a2].map(d => this.AttrTypeMap[d]),
                            size: this.CurExDataset.length,
                        },
                    }).then((response) => {
                        let data = response.data;
                        resolve(data.ret[1]);
                    });
                });
            } else {
                // 非敏感查询 / issue query
                let [bins, queryRes] = this.getQueryRes(
                    QueryAttrNames[0],
                    QueryContent,
                    this.CurExDataset,
                    ""
                );
                let axisAttr = [QueryAttrNames[0], QueryContent, QueryAttrNames[1]];
                let binKeys = Object.keys(queryRes);

                for (let idx in bins) {
                    let [, secondQueryRes] = this.getQueryRes(
                        QueryAttrNames[1],
                        QueryContent,
                        bins[+idx],
                        this.getNoiseKey(QueryAttrNames[0], binKeys[+idx])
                    );
                    queryRes[binKeys[+idx]] = secondQueryRes;
                }
                // 获得属性的真实相关性
                if (!is) {
                    axios({
                        method: "post",
                        url: "http://127.0.0.1:8000/Utils/GetAttrCorrelation/",
                        data: {
                            queryRes: queryRes,
                            'AttrTypeList': QueryAttrs.map(d => this.AttrTypeMap[d])
                        },
                    }).then((response) => {
                        let copyAttrList = JSON.parse(JSON.stringify(QueryAttrs));
                        let NodeNameList = copyAttrList.sort();
                        let lineName = `${NodeNameList[0]}±${NodeNameList[1]}`;
                        this.VerifiedCorrelationMap[lineName] =
                            response.data.correlation.toFixed(2);
                        let lineSelected = d3.select(`#${lineName}`).classed("chosenQuery");
                        if(lineSelected) {
                            d3.select(`#${lineName}text`).text(
                                `${this.SimulatedCorrelationMap[lineName]}|${this.VerifiedCorrelationMap[lineName]}`
                            );
                        }
                    });
                }
                return new Promise((resolve) => {
                    resolve([queryRes, axisAttr]);
                });
            }
        },
        executeTriPAttrQuery(QueryAttrs, QueryContent, isSimulation) {
            // if(this.isSimulation) {

            // } else {
            let QueryAttrNames = QueryAttrs;
            let finalQueryRes = {};
            let bins = [];
            let qanIdx = 0;
            [bins, finalQueryRes] = this.getQueryRes(
                QueryAttrNames[qanIdx],
                QueryContent,
                this.CurExDataset,
                ""
            );
            let binKeys = Object.keys(finalQueryRes);
            for (let idx in bins) {
                this.executeQueryMeta(
                    QueryAttrs,
                    QueryContent,
                    bins[+idx],
                    1,
                    QueryAttrs.length - 1,
                    finalQueryRes,
                    binKeys[+idx]
                );
            }
            return new Promise(resolve => {
                resolve([finalQueryRes]);
            });
            // }
        },
        executeQueryMeta(
            QueryAttrs,
            QueryContent,
            dataset,
            depth,
            maxDepth,
            ret,
            binKey
        ) {
            if (depth > maxDepth) {
                return;
            }
            let [bins, QueryRes] = this.getQueryRes(
                QueryAttrs[depth],
                QueryContent,
                dataset,
                ""
                // this.getNoiseKey(QueryAttrs[0], binKeys[+idx])
            );
            ret[binKey] = QueryRes;
            let binKeys = Object.keys(QueryRes);
            for (let idx in bins) {
                this.executeQueryMeta(
                    QueryAttrs,
                    QueryContent,
                    bins[+idx],
                    depth + 1,
                    maxDepth,
                    QueryRes,
                    binKeys[+idx]
                );
            }
        },
        // 范围取整函数
        roundedScope(dataMin, dataMax) {
            return [Math.floor(dataMin), Math.ceil(dataMax)];
        },
        // input: d: object
        // 目前采用的是 d3.autoType 识别的效果
        // 相对来说不会那么准确，后续如果需要优化，则可以用手动识别的方式
        getAttrType(d) {
            let AttrTypeMap = Object.keys(d).reduce((ret, attribute) => {
                const type = typeof d[attribute];
                ret[attribute] =
                    type === "number" ? "#" : type === "string" ? "A" : "T";
                return ret;
            }, {});
            return AttrTypeMap;
        },
        // 直方图数据生成器
        histogramDataGenerator(data, value) {
            let domain = this.AttrQueryBinRangeMap[value];
            let threshold = [...domain];
            threshold.pop();
            let histogramDataGenerator = d3
                .histogram()
                .value(function (d) {
                    return d[value];
                })
                .domain([domain[0], domain[domain.length - 1]]) // 指定数据的范围
                .thresholds(threshold);

            return histogramDataGenerator(data);
        },
        // 封装 getHQueryRes 和 getCQueryRes
        getQueryRes(QueryAttrName, QueryContent, data, PreNoiseKey) {
            if (this.AttrTypeMap[QueryAttrName] === "#") {
                let bins = this.histogramDataGenerator(data, QueryAttrName);
                let queryRes = this.getHQueryRes(
                    bins,
                    QueryAttrName,
                    QueryContent,
                    PreNoiseKey
                ); // histogram query
                return [bins, queryRes];
            } else if (this.AttrTypeMap[QueryAttrName] === "A") {
                let groupedData = d3.group(data, (d) => d[QueryAttrName]);
                let bins = Array.from(groupedData);
                let binRange = bins.map((bin) => bin[0]);
                // 按字典排序
                let temp = [];
                for (let category of this.AttrRangeMap[QueryAttrName]) {
                    if(bins.find(d=>d[0]===category || +d[0] === +category)) {
                        temp.push([category, bins.find(d=>d[0]===category || +d[0] === +category )[1]]);
                    } else {
                        temp.push([category, []])
                    }
                }
                bins = temp;
                let queryRes = this.getCQueryRes(
                    bins,
                    QueryAttrName,
                    QueryContent,
                    PreNoiseKey
                ); // categorical query
                bins = bins.map((bin) => bin[1]);
                return [bins, queryRes];
            }
        },
        // get histogram query result
        getHQueryRes(bins, QueryAttrName, QueryContent, PreNoiseKey) {
            let binsData;
            if (this.isSimulation && this.AttrSensitive[QueryAttrName]) {
                return JSON.parse(
                    JSON.stringify(this.simulateDataRecord[QueryAttrName])
                ); //this.getSimulationData(bins);
            } else {
                binsData = bins.map((bin, i) => {
                    // 多分布
                    if (Array.isArray(bin[0])) {
                        return [];
                    } else {
                        let ret;
                        if (QueryContent === "#COUNT") {
                            ret = bin.length;
                        } else {
                            ret = d3.sum(bin, (d) => d[QueryContent]);
                        }
                        // let curNoiseKey, finalNoiseKey;
                        // curNoiseKey = this.getNoiseKey(
                        //   QueryAttrName,
                        //   `${bin.x0}-${bin.x1}`,
                        //   "#"
                        // );
                        // if (PreNoiseKey[0] < curNoiseKey[0]) {
                        //   finalNoiseKey = PreNoiseKey
                        //     ? PreNoiseKey + "-" + curNoiseKey
                        //     : curNoiseKey;
                        // } else {
                        //   finalNoiseKey = PreNoiseKey
                        //     ? curNoiseKey + "-" + PreNoiseKey
                        //     : curNoiseKey;
                        // }
                        // ret += this.NoiseMap[finalNoiseKey];
                        // if (this.NoiseMap[finalNoiseKey] === undefined) {
                        //   if (curNoiseKey === "c-1") {
                        //     console.log("xxx");
                        //   }
                        //   console.log(curNoiseKey, finalNoiseKey, "undefined ");
                        // }
                        return ret;
                    }
                });
            }
            let binsMap = bins.reduce((pre, cur, i) => {
                pre[`${cur.x0}-${cur.x1}`] = binsData[i];
                return pre;
            }, {});
            return binsMap;
        },
        // get categorical query result
        getCQueryRes(bins, QueryAttrName, QueryContent, PreNoiseKey) {
            let binsData;
            if (this.isSimulation && this.AttrSensitive[QueryAttrName]) {
                return JSON.parse(
                    JSON.stringify(this.simulateDataRecord[QueryAttrName]))
            } else {
                binsData = bins.map((bin) => {
                    // 多分布
                    if (Array.isArray(bin[1][0])) {
                        return [];
                    } else {
                        let ret;
                        if (QueryContent === "#COUNT") {
                            ret = bin[1].length;
                        } else {
                            ret = d3.sum(bin[1], (d) => d[QueryContent]);
                        }
                        return ret;
                    }
                });
            }
            let binsMap = bins.reduce((pre, cur, i) => {
                pre[`${cur[0]}`] = binsData[i];
                return pre;
            }, {});
            return binsMap;
        },
        getNoiseKey(QueryAttrName, Data, Type) {
            if (Type === undefined) {
                Type = this.AttrTypeMap[QueryAttrName];
            }
            if (Type === "A") {
                let pre = this.CurQuery.indexOf(QueryAttrName);
                let tail = this.AttrRangeMap[QueryAttrName].indexOf(Data);
                if (`${String.fromCharCode(pre + 97)}${tail}` === "c-1") {
                    console.log("xxx");
                }
                return `${String.fromCharCode(pre + 97)}${tail}`;
            } else {
                let data = +Data.split("-")[0];
                let pre = this.CurQuery.indexOf(QueryAttrName);
                let tail = this.AttrBinRangeMap[QueryAttrName].indexOf(data);
                if (`${String.fromCharCode(pre + 97)}${tail}` === "c-1") {
                    console.log("xxx");
                }
                return `${String.fromCharCode(pre + 97)}${tail}`;
            }
        },
        getSimulationData(bins) {
            if (this.CurModal === "up") {
                let cur = 0;
                let binsData = bins.map((bin) => {
                    cur += 10;
                    return cur;
                });
                return binsData;
            }
        },

        dblclickDataColumn(column) {
            if (this.ColumnDbClickMap[column]) {
                this.CurQueryList.splice(this.CurQueryList.indexOf([column], 1));
            } else {
                this.CurQueryList.push([column]);
            }
            this.ColumnDbClickMap[column] = !this.ColumnDbClickMap[column];
        },
        updateAttrHistogram(thisNodeName, data) {
            this.CurThisNodeName = thisNodeName;
            d3.selectAll(".intentNode circle").classed("histogramAttr", false);
            d3.select(`#intentNode${thisNodeName} circle`).attr(
                "class",
                "histogramAttr"
            );

            return new Promise((resolve) => {
                let prom;
                if (this.simulateDataRecord[thisNodeName]) {
                    prom = new Promise((resolve) => {
                        resolve([this.simulateDataRecord[thisNodeName]]);
                    });
                } else {
                    prom = this.executeQuery([thisNodeName], "#COUNT", 0);
                }
                prom.then((ret) => {
                    let attrHistogram = ret[0];
                    let isSensitive = this.AttrSensitive[thisNodeName];
                    let histogramContainer = d3.select(".CurAttrHistogram");
                    histogramContainer.selectAll(".barRectG").remove();
                    histogramContainer.selectAll("text").remove();
                    let svg = d3.select(".DBAttrBody");
                    let { height: gHeight, width: gWidth } = histogramContainer
                        .select("rect")
                        .node()
                        .getBoundingClientRect();
                    let padding = 20;
                    let rectData = Object.entries(attrHistogram);
                    let xDomain = rectData.map(([category, value]) => category);

                    let isNumericalX = this.AttrTypeMap[thisNodeName] == '#';
                    let yRange = [gHeight - padding * 2, padding * 2];
                    let [xScale, tickValues, bandwidthScale, bandwidth] = this.GetScale(
                        isNumericalX,
                        xDomain,
                        [padding * 3, gWidth - padding],
                        false
                    );
                    const yScale = d3
                        .scaleLinear()
                        .domain([0, d3.max(rectData, (d) => d[1])])
                        .range(yRange);
                    const xAxis = d3
                        .axisBottom(xScale)
                        .tickSizeOuter(10)
                        .tickValues(tickValues);

                    if(isNumericalX) {
                        xAxis.tickFormat(d => d > 1000 ? (d/1000).toFixed(0) + 'k' : d);
                    }

                    histogramContainer.select(".tickLineG").remove();
                    let tickLineG = histogramContainer
                        .append("g")
                        .attr("class", "tickLineG");
                    let tickLineData = [];
                    let step = (yRange[0] - yRange[1]) / 5;
                    for (let i = yRange[1] + step; i < yRange[0]; i += step) {
                        tickLineData.push(i);
                    }
                    // let yDomain = yScale.domain();
                    // let step = (yDomain[1] - yDomain[0]) / 5;
                    // let pD = 0;
                    // for (let i = yDomain[0] + step; i < yDomain[1]; i += step) {
                    //   if (
                    //     i == yDomain[0] + step ||
                    //     Math.floor(i).toString().length >
                    //       Math.floor(i - step).toString().length
                    //   ) {
                    //     pD += 1;
                    //   }
                    //   console.log(i, this.roundToHighestPlace(Math.floor(i), pD));

                    //   tickLineData.push(this.roundToHighestPlace(Math.floor(i), pD));
                    // }

                    tickLineG
                        .selectAll(".tickLine")
                        .data(tickLineData)
                        .join("line")
                        .attr("class", "tickLine")
                        .attr("x1", xScale.range()[0])
                        .attr("x2", xScale.range()[1])
                        .attr("y1", (d) => d)
                        .attr("y2", (d) => d)
                        .attr("stroke", this.BaseColorMap["grey-light"])
                        .attr("stroke-width", 2)
                        .attr("stroke-dasharray", "5,5"); // 可选，添加虚线效果
                    // tickLineG
                    //   .selectAll(".tickLineText")
                    //   .data(tickLineData)
                    //   .join("text")
                    //   .attr("class", "tickLineText legendText")
                    //   .attr("x", xScale.range()[0] - 0.5 * padding)
                    //   .attr("y", (d) => yScale(d) + 5)
                    //   .attr("text-anchor", "end")
                    //   .text((d) => d); // 可选，添加虚线效果

                    histogramContainer.select(".xAxis").remove();
                    histogramContainer
                        .append("g")
                        .attr("class", "xAxis")
                        .attr("transform", `translate(0, ${yRange[0] + 5})`)
                        .call(xAxis);
                    histogramContainer.select("marker").remove();
                    histogramContainer
                        .append("marker")
                        .attr("id", "arrow")
                        .attr("markerUnits", "strokeWidth")
                        .attr("viewBox", "0 0 12 12")
                        .attr("refX", 6)
                        .attr("refY", 6)
                        .attr("markerWidth", 12)
                        .attr("markerHeight", 12)
                        .attr("orient", "auto")
                        .append("path")
                        .attr("d", "M2,2 L10,6 L2,10 L6,6 L2,2")
                        .attr("fill", this.BaseColorMap["grey-normal"]);
                    histogramContainer
                        .select(".xAxis")
                        .select("path")
                        .attr("d", (d) => {
                            let pathD = histogramContainer.select(`.xAxis path`).attr("d");
                            pathD = pathD.replace("V10", "");
                            pathD = pathD.replace(",10V", ",0V");
                            return pathD;
                        })
                        .attr("stroke", this.BaseColorMap["grey-normal"])
                        .attr("marker-end", "url(#arrow)");

                    let barRectContainer = histogramContainer
                        .append("g")
                        .attr("class", "barRectContainer");
                    let barRectG = barRectContainer
                        .selectAll(".barRect")
                        .data(rectData)
                        .join("g")
                        .attr("class", "barRectG");
                    barRectG
                        .append("rect")
                        .attr("class", "barRect")
                        .attr("x", (d) =>
                            isNumericalX
                                ? xScale(Number(d[0].split("-")[0])) + 5
                                : xScale(d[0]) + 5
                        )
                        .attr("y", (d) => yScale(d[1]))
                        .attr(
                            "width",
                            (xScale.range()[1] - xScale.range()[0]) / xDomain.length - 10
                        )
                        .attr("height", (d) => yRange[0] - yScale(d[1]))
                        .attr("fill", this.BaseColorMap["grey-normal"])
                        .attr("fill-opacity", 0.5);

                    // Drag function
                    if (isSensitive) {
                        let VueThis = this;
                        const drag = d3.drag().on("drag", function (e, d, i) {
                            let moveY = Math.min(yRange[0], e.y);
                            moveY = Math.max(yRange[1], moveY);
                            // 修改 d
                            d[1] = yScale.invert(moveY);
                            attrHistogram[d[0]] = d[1];
                            // 移动图形
                            d3.select(this).attr("cy", moveY);
                            d3.select(this.previousSibling)
                                .attr("y", moveY)
                                .attr("height", yRange[0] - moveY);
                            VueThis.updateSimulatedAttrLineChart(thisNodeName, attrHistogram);
                        });

                        barRectG
                            .append("circle")
                            .attr("class", "MoveCircle")
                            .attr("cx", (d) =>
                                isNumericalX
                                    ? xScale(Number(d[0].split("-")[0])) +
                                    5 +
                                    ((xScale.range()[1] - xScale.range()[0]) / xDomain.length -
                                        10) /
                                    2
                                    : xScale(d[0]) +
                                    5 +
                                    ((xScale.range()[1] - xScale.range()[0]) / xDomain.length -
                                        10) /
                                    2
                            )
                            .attr("cy", (d) => yScale(d[1]))
                            .attr("r", 5)
                            .attr("fill", this.BaseColorMap["grey-normal"])
                            .attr("cursor", "pointer")
                            .call(drag);
                    }

                    histogramContainer
                        .append("text")
                        .attr("x", 10)
                        .attr("y", 20)
                        .text(thisNodeName);

                    // 如果是敏感属性，则进行特殊处理（包括可修改，保存修改后的数据）
                    if (isSensitive) {
                        // 添加
                    }
                    resolve(attrHistogram);
                });
            });
        },
        updateVerifiedAttrLineChart(nodeName, data) {
            let attrHistogram = data;
            let histogramContainer = d3.select(`#intentNode${nodeName}`);
            histogramContainer.selectAll(".VerifiedPath").remove();
            let svg = d3.select(".DBAttrBody");
            let [gHeight, gWidth] = [50, 50];
            let translate = +d3.select(`#intentNode${nodeName} circle`).attr("cx");
            let padding = 20;
            let rectData = Object.entries(attrHistogram);
            let isNumericalX = this.AttrTypeMap[nodeName] == '#';
            if (!isNumericalX) {
                let temp = [];
                let idx = 0;
                for (let [category, value] of rectData) {
                    if (idx == 0) {
                        temp.push([category, value]);
                        temp.push([`a${idx}`, value]);
                        idx += 1;
                    } else {
                        temp.push([`a${idx - 1}`, value]);
                        temp.push([category, value]);
                        if(idx !== rectData.length-1) {
                            temp.push([`a${idx}`, value]);
                        }
                        idx += 1;
                    }
                }
                rectData = temp;
            }
            let xDomain = [...new Set(rectData.map(([category, value]) => category))];

            let yRange = [gHeight - 20, 0];
            let [xScale, tickValues, bandwidthScale, bandwidth] = this.GetScale(
                isNumericalX,
                xDomain,
                [translate - gWidth / 2, translate + gWidth / 2],
                true
            );
            let yScale;
            if (this.AttrDistributionYscaleMap[nodeName]) {
                yScale = this.AttrDistributionYscaleMap[nodeName];
                // let lastDomainMin = yScale.domain()[0];
                let lastDomainMax = yScale.domain()[1];
                yScale.domain([
                    0,
                    Math.max(
                        d3.max(rectData, (d) => d[1]),
                        lastDomainMax
                    ),
                ]);
            } else {
                yScale = d3
                    .scaleLinear()
                    .domain([0, d3.max(rectData, (d) => d[1])])
                    .range(yRange);
                this.AttrDistributionYscaleMap[nodeName] = yScale;
            }
            let minY;
            if (this.NodeMinY[nodeName] === undefined) {
                minY = this.NodeMinY[nodeName] = d3.min(rectData, (d) => d[1]);
            } else {
                let nodeMinY = this.NodeMinY[nodeName];
                minY = Math.min(
                    d3.min(rectData, (d) => d[1]),
                    nodeMinY
                );
                this.NodeMinY[nodeName] = minY;
            }
            let line = d3
                .line()
                .x((d) =>
                    isNumericalX
                        ? xScale((+d[0].split("-")[0] + +d[0].split("-")[1]) / 2)
                        : xScale(d[0]) + bandwidth / 2
                )
                .y((d) => yScale(d[1]) + (yRange[0] - yScale(minY)) / 2);
            let quartileNoise = this.calculateQuantile(
                0,
                1 / this.PreQueryEpsilon,
                0.475
            );
            // histogramContainer
            //   .append("path")
            //   .datum(rectData)
            //   .attr("class", "VerifiedPathBgc")
            //   .attr("d", line)
            //   .attr("stroke", this.BaseColorMap["grey-normal"])
            //   .attr("stroke-width", gHeight - 20 - yScale(quartileNoise))
            //   .attr("fill", "none");
            histogramContainer
                .append("path")
                .datum(rectData)
                .attr("class", "VerifiedPath")
                .attr("d", line)
                .attr("stroke", this.BaseColorMap["grey-normal"])
                .attr("stroke-width", Math.max(gHeight - 20 - yScale(quartileNoise), 2))
                .attr("fill", "none");
        },
        updateSimulatedAttrLineChart(nodeName, data) {
            let attrHistogram = data;
            let histogramContainer = d3.select(`#intentNode${nodeName}`);
            histogramContainer.selectAll(".SimulatedPath").remove();
            let svg = d3.select(".DBAttrBody");
            let [gHeight, gWidth] = [50, 50];
            let translate = +d3.select(`#intentNode${nodeName} circle`).attr("cx");
            let padding = 20;
            let rectData = Object.entries(attrHistogram);
            let isNumericalX = this.AttrTypeMap[nodeName] == '#';
            let idx = 0;
            if (!isNumericalX) {
                let temp = [];
                for (let [category, value] of rectData) {
                    if (idx == 0) {
                        temp.push([category, value]);
                        idx += 1;
                    } else {
                        temp.push([category, rectData[idx-1][1]]);
                        temp.push([category, value]);
                        idx += 1;
                    }
                }
                temp.push(['_a_', rectData[idx-1][1]])
                rectData = temp;
            }
            let xDomain = [...new Set(rectData.map(([category, value]) => category))];

            let yRange = [gHeight - 20, 0];
            let [xScale, tickValues, bandwidthScale, bandwidth] = this.GetScale(
                isNumericalX,
                xDomain,
                [translate - gWidth / 2, translate + gWidth / 2],
                true
            );
            let yScale;
            if (this.AttrDistributionYscaleMap[nodeName]) {
                yScale = this.AttrDistributionYscaleMap[nodeName];
                // let lastDomainMin = yScale.domain()[0];
                let lastDomainMax = yScale.domain()[1];
                yScale.domain([
                    0,
                    Math.max(
                        d3.max(rectData, (d) => d[1]),
                        lastDomainMax
                    ),
                ]);
            } else {
                yScale = d3
                    .scaleLinear()
                    .domain([0, d3.max(rectData, (d) => d[1])])
                    .range(yRange);
                this.AttrDistributionYscaleMap[nodeName] = yScale;
            }
            let minY;
            if (this.NodeMinY[nodeName] === undefined) {
                minY = this.NodeMinY[nodeName] = d3.min(rectData, (d) => d[1]);
            } else {
                let nodeMinY = this.NodeMinY[nodeName];
                minY = Math.min(
                    d3.min(rectData, (d) => d[1]),
                    nodeMinY
                );
                this.NodeMinY[nodeName] = minY;
            }
            let line = d3
                .line()
                .x((d) =>
                    isNumericalX
                        ? xScale((+d[0].split("-")[0] + +d[0].split("-")[1]) / 2)
                        : xScale(d[0]) + bandwidth / 2
                )
                .y((d) => yScale(d[1]) + (yRange[0] - yScale(minY)) / 2);
            histogramContainer
                .append("path")
                .datum(rectData)
                .attr("class", "SimulatedPath")
                .attr("d", line)
                .attr(
                    "stroke",
                    this.AttrSensitive[nodeName]
                        ? this.BaseColorMap["grey-light"]
                        : this.BaseColorMap["grey-normal"]
                )
                .attr("stroke-width", 2)
                .attr("fill", "none");
        },

        readData() {
            return new Promise(resolve => {
                d3.csv(`./data/${this.CurDatabase}/${this.CurDatabase}.csv`, d3.autoType).then((dataset) => {
                    this.CurExDataset = this.Dataset = dataset;
                    this.DatasetColumns = dataset.columns;
                    let svgWidth = 550;

                    this.$nextTick(() => {
                        let svg = d3.select(".DBAttrBody");
                        let sumWidth = 0;
                        let curDepthIdx = 0;
                        svg.selectAll(".AttrRect").each(function (d, i, a) {
                            const textWidth = this.nextElementSibling.getBBox().width;
                            d3.select(this).attr("width", textWidth + 10);
                            d3.select(this.nextElementSibling).attr("x", textWidth / 2 + 5);
                            // circle
                            d3.select(this.parentNode.nextElementSibling.firstElementChild).attr(
                                "cx",
                                textWidth / 2 + 5
                            );
                            // circle text
                            d3.select(
                                this.parentNode.nextElementSibling.firstElementChild
                                    .nextElementSibling
                            ).attr("x", textWidth / 2 + 5 + 40);

                            d3.select(`#AttrRectBg${i}`).attr("width", textWidth + 10);
                            d3.select(`#AttrTextBg${i}`).attr("x", textWidth / 2 + 5);

                            if (
                                Math.ceil(sumWidth / svgWidth) !=
                                Math.ceil((sumWidth + textWidth + 10 + 20) / svgWidth)
                            ) {
                                let rawWidth = sumWidth;
                                sumWidth = Math.ceil(sumWidth / svgWidth) * svgWidth;
                                // 实现两端对齐
                                let x = (sumWidth - rawWidth) / (i - curDepthIdx - 1);
                                for (let j = curDepthIdx + 1; j < i; j++) {
                                    let translateStr = d3
                                        .select(a[j].parentNode.parentNode)
                                        .attr("transform");
                                    const matches = translateStr.match(
                                        /translate\((-?[\d.]+), (-?[\d.]+)\)/
                                    );
                                    console.log(matches);
                                    d3.select(a[j].parentNode.parentNode).attr(
                                        "transform",
                                        `translate(${
                                            parseFloat(matches[1]) + x * (j - curDepthIdx)
                                        }, ${parseFloat(matches[2])})`
                                    );
                                    d3.select(`#DBAttrItemBg${j}`).attr(
                                        "transform",
                                        `translate(${
                                            parseFloat(matches[1]) + x * (j - curDepthIdx)
                                        }, ${parseFloat(matches[2])})`
                                    );
                                }

                                curDepthIdx = i;
                            }
                            d3.select(this.parentNode.parentNode).attr(
                                "transform",
                                `translate(${sumWidth % svgWidth}, ${
                                    10 + 40 * Math.floor(sumWidth / svgWidth)
                                })`
                            );
                            d3.select(`#DBAttrItemBg${i}`).attr(
                                "transform",
                                `translate(${sumWidth % svgWidth}, ${
                                    10 + 40 * Math.floor(sumWidth / svgWidth)
                                })`
                            );

                            sumWidth += textWidth + 10 + 20;
                            console.log(textWidth, sumWidth);
                        });
                    });

                    this.DatasetColumns.forEach((d) => {
                        this.ColumnDbClickMap[d] = false;
                    });
                    this.AttrTypeMap = this.getAttrType(dataset[0]);
                    console.log(this.AttrTypeMap);
                    for (let column of this.DatasetColumns) {
                        if (this.AttrTypeMap[column] === "#") {
                            let [max, min] = [
                                d3.max(dataset, (d) => d[column]),
                                d3.min(dataset, (d) => d[column]),
                            ];
                            console.log(column, [max, min]);
                        }
                    }
                    d3.json(`./data/${this.CurDatabase}/attr_mess.json`).then((AttrMessMap) => {
                        this.AttrMessMap = AttrMessMap;
                        d3.json(`./data/${this.CurDatabase}/sensitive_attr.json`).then((data) => {
                            this.AttrSensitive = {};
                            for (let column of this.DatasetColumns) {
                                this.AttrSensitive[column] = data.includes(column);
                            }
                            console.log(this.AttrSensitive);

                            d3.json(`./data/${this.CurDatabase}/special_attr.json`).then(specialAttr => {
                                this.specialAttrList = specialAttr;
                                d3.json(`./data/${this.CurDatabase}/categorical_attr.json`).then(categoricalAttrRange => {
                                    d3.csv(`./data/${this.CurDatabase}/attr_range.csv`, d3.autoType).then((data) => {
                                        this.AttrRangeMap = data.reduce((pre, cur) => {
                                            pre[cur["attribute"]] = [cur["min"], cur["max"]];
                                            return pre;
                                        }, {});
                                        this.minAttrGranularityList = data.reduce((pre, cur) => {
                                            pre[cur["attribute"]] = cur["granularity"];
                                            return pre;
                                        }, {});
                                        for (let attr in categoricalAttrRange) {
                                            this.AttrTypeMap[attr] = 'A';
                                        }

                                        for (let attr of this.DatasetColumns) {
                                            if (this.AttrTypeMap[attr] === "A") {
                                                this.AttrRangeMap[attr] = categoricalAttrRange[attr];
                                                // this.AttrRangeMap[attr] = [
                                                //     ...new Set(this.Dataset.map((d) => d[attr])),
                                                // ];
                                            }
                                        }

                                        for (let attr of this.DatasetColumns) {
                                            if (this.AttrTypeMap[attr] === "#") {
                                                let attrRange = this.AttrRangeMap[attr];
                                                if (attrRange === undefined) {
                                                    this.AttrTypeMap[attr] = "A";
                                                    this.AttrRangeMap[attr] = categoricalAttrRange[attr];
                                                    continue;
                                                }
                                                let minAttrGranularity = this.minAttrGranularityList[attr];
                                                let temp = [];
                                                for (
                                                    let i = attrRange[0];
                                                    i <= attrRange[1];
                                                    i += minAttrGranularity
                                                ) {
                                                    temp.push(i);
                                                }
                                                this.AttrBinRangeMap[attr] = temp;
                                                this.AttrBinRangeShowMap[attr] = {};
                                            } else {
                                                this.AttrBinRangeMap[attr] = this.AttrRangeMap[attr];
                                                this.AttrBinRangeShowMap[attr] = {};
                                            }
                                        }
                                        this.AttrQueryBinRangeMap = JSON.parse(
                                            JSON.stringify(this.AttrBinRangeMap)
                                        );
                                    });
                                })
                                resolve();
                            })
                        });
                    })

                });
            })

        },
        setMoveNodeEvent() {
            let VueThis = this;
            // 初始化数据
            VueThis.rectWHMap = {};
            VueThis.AttrIntentMap = {};
            d3.selectAll(".DBAttrItem").call(
                d3
                    .drag()
                    .on("start", function (event) {
                        d3.select(this).raise().classed("active", true);
                        console.log(event);
                    })
                    .on("drag", function (event) {
                        let thisNode = this;
                        let thisNodeName = d3.select(thisNode).attr("name");
                        let [x, y] = [event.x, event.y];
                        let rectW;
                        let rectH;
                        if (VueThis.rectWHMap[thisNodeName] === undefined) {
                            rectW = parseFloat(d3.select(this).select("rect").attr("width"));
                            rectH = parseFloat(d3.select(this).select("rect").attr("height"));
                            VueThis.rectWHMap[thisNodeName] = [rectW, rectH];
                        } else {
                            [rectW, rectH] = VueThis.rectWHMap[thisNodeName];
                        }

                        console.log(rectW, rectH);
                        d3.select(this).attr(
                            "transform",
                            `translate(${x - rectW / 2},${y - rectH / 2})`
                        );
                        let LineContainer = d3.select(".LineContainer");
                        let isNewNode = !d3.select(thisNode).classed("ContactedAttr");
                        // 还少了一个右下角的条件
                        if (x > 15 && y > 220) {
                            VueThis.AttrIntentMap[thisNodeName] = true
                            if (isNewNode) {
                                // 新增连线
                                d3.selectAll(".ContactedAttr").each(function () {
                                    let thatNode = this;
                                    let thatNodeName = d3.select(thatNode).attr("name");
                                    let NodeNameList = [thisNodeName, thatNodeName].sort();
                                    let lineName = `${NodeNameList[0]}±${NodeNameList[1]}`;
                                    if (VueThis.rectWHMap[thatNodeName] === undefined) {
                                        let rectW = parseFloat(
                                            d3.select(this).select("rect").attr("width")
                                        );
                                        let rectH = parseFloat(
                                            d3.select(this).select("rect").attr("height")
                                        );
                                        VueThis.rectWHMap[thatNodeName] = [rectW, rectH];
                                    }
                                    let isSensitiveQuery =
                                        VueThis.AttrSensitive[NodeNameList[0]] ||
                                        VueThis.AttrSensitive[NodeNameList[1]];
                                    const newLine = LineContainer.append("line")
                                        .attr("id", lineName)
                                        .attr("stroke", VueThis.BaseColorMap["grey-normal-opacity"])
                                        .attr("stroke-width", 5)
                                        .attr("stroke-dasharray", "5,2")
                                        .on("click", function (event) {
                                            let isChosen = d3.select(this).classed("chosenQuery");
                                            d3.select(this).classed("chosenQuery", !isChosen);
                                            if (isChosen) {
                                                d3.select(this)
                                                    .attr("stroke-dasharray", "5,2")
                                                    .attr("stroke", VueThis.BaseColorMap["grey-normal-opacity"]);
                                                VueThis.CurQueryList.splice(
                                                    VueThis.CurQueryList.findIndex(
                                                        (d) =>
                                                            JSON.stringify(d) ===
                                                            JSON.stringify(lineName.split("±"))
                                                    ),
                                                    1
                                                );
                                                LineContainer.select(`#${lineName}text`).text('');
                                            } else {
                                                VueThis.CurQueryList.push(lineName.split("±"));
                                                // VueThis.CurQuery = VueThis.CurQueryList[0];
                                                d3.select(this)
                                                    .attr("stroke-dasharray", null)
                                                    .attr("stroke", VueThis.BaseColorMap["grey-normal-opacity"]);
                                                if(VueThis.specialAttrList.includes(NodeNameList[0]) || VueThis.specialAttrList.includes(NodeNameList[1])) {
                                                    LineContainer.select(`#${lineName}text`).text('');
                                                }
                                                else {
                                                    LineContainer.select(`#${lineName}text`).text(VueThis.SimulatedCorrelationMap[lineName]);
                                                }
                                            }
                                        });
                                    let [x1, y1] = d3
                                        .select(thisNode)
                                        .attr("transform")
                                        .match(/-?[\d.]+/g);
                                    let [x2, y2] = d3
                                        .select(thatNode)
                                        .attr("transform")
                                        .match(/-?[\d.]+/g);
                                    let [rectW1, rectH1] = VueThis.rectWHMap[thisNodeName];
                                    let [rectW2, rectH2] = VueThis.rectWHMap[thatNodeName];
                                    x1 = +x1 + rectW1 / 2 + 15;
                                    y1 = +y1 + rectH1 / 2 + 30;
                                    x2 = +x2 + rectW2 / 2 + 15;
                                    y2 = +y2 + rectH2 / 2 + 30;
                                    newLine
                                        .attr("x1", x1)
                                        .attr("y1", y1)
                                        .attr("x2", x2)
                                        .attr("y2", y2);

                                    // 如果是敏感查询，则显示 请输入 的文字
                                    if (isSensitiveQuery) {
                                        VueThis.SimulatedCorrelationMap[lineName] = 0;
                                        LineContainer.append("text")
                                            .attr("id", lineName + "text")
                                            .attr("x", (x1 + x2) / 2)
                                            .attr("y", (y1 + y2) / 2+5)
                                            .attr("text-anchor", "middle")
                                            .text('')
                                            .on("dblclick", function () {
                                                let correlation = +d3.select(this).text();
                                                VueThis.editText(lineName, correlation);
                                                if (!VueThis.AttrSensitive[thisNodeName]) {
                                                    VueThis.CurLineNonSensitiveAttr = thisNodeName;
                                                    VueThis.CurLineSensitiveAttr = thatNodeName;
                                                } else {
                                                    VueThis.CurLineNonSensitiveAttr = thatNodeName;
                                                    VueThis.CurLineSensitiveAttr = thisNodeName;
                                                }
                                            });
                                    } else {
                                        // VueThis.isSimulation = false;
                                        VueThis.executeQuery(NodeNameList, "#COUNT").then(data => {
                                            axios({
                                                method: "post",
                                                url: "http://127.0.0.1:8000/Utils/GetAttrCorrelation/",
                                                data: {
                                                    queryRes: data[0],
                                                    'AttrTypeList': [thisNodeName, thatNodeName].map(d => VueThis.AttrTypeMap[d]),
                                                },
                                            }).then((response) => {
                                                // VueThis.isSimulation = true;
                                                VueThis.SimulatedCorrelationMap[lineName] = response.data.correlation.toFixed(2);
                                                VueThis.VerifiedCorrelationMap[lineName] =
                                                    response.data.correlation.toFixed(2);
                                                LineContainer.append("text")
                                                    .attr("id", lineName + "text")
                                                    .attr("x", (x1 + x2) / 2)
                                                    .attr("y", (y1 + y2) / 2+5)
                                                    .attr("text-anchor", "middle")
                                                    .text('')
                                            });
                                        })
                                    }
                                    if(VueThis.specialAttrList.includes(NodeNameList[0]) || VueThis.specialAttrList.includes(NodeNameList[1])) {
                                        VueThis.SimulatedCorrelationMap[lineName] = 0;
                                    }
                                });

                                // 展示当前查询的分布
                                if (!VueThis.AttrSensitive[thisNodeName]) {
                                    VueThis.updateAttrHistogram(thisNodeName).then(
                                        (simulateData) => {
                                            VueThis.simulateDataRecord[thisNodeName] = simulateData;
                                            VueThis.updateSimulatedAttrLineChart(
                                                thisNodeName,
                                                simulateData
                                            );
                                        }
                                    );
                                } else {
                                    // 敏感属性的情况
                                    if (VueThis.simulateDataRecord[thisNodeName]) {
                                        VueThis.updateAttrHistogram(
                                            thisNodeName,
                                            VueThis.simulateDataRecord[thisNodeName]
                                        );

                                        VueThis.updateSimulatedAttrLineChart(
                                            thisNodeName,
                                            simulateData
                                        );
                                    } else {
                                        let simulateData = {};
                                        let binRange = VueThis.AttrBinRangeMap[thisNodeName];
                                        let baseVal =
                                            VueThis.CurExDataset.length / (binRange.length - 1);
                                        if(VueThis.AttrTypeMap[thisNodeName] === '#') {
                                            for (let i in binRange) {
                                                let idx = +i;
                                                if (idx !== 0) {
                                                    let noise = (Math.random() * baseVal) / 2;
                                                    simulateData[binRange[idx - 1] + "-" + binRange[idx]] =
                                                        baseVal + noise;
                                                }
                                            }
                                        }
                                        else {
                                            for (let i in binRange) {
                                                let idx = +i;
                                                let noise = (Math.random() * baseVal) / 2;
                                                simulateData[binRange[idx]] =
                                                    baseVal + noise;

                                            }
                                        }
                                        VueThis.simulateDataRecord[thisNodeName] = simulateData;
                                        VueThis.SensitiveAttrSimulate[thisNodeName] = simulateData;
                                        VueThis.updateAttrHistogram(thisNodeName, simulateData);
                                        VueThis.updateSimulatedAttrLineChart(
                                            thisNodeName,
                                            simulateData
                                        );
                                    }
                                }
                            } else {
                                // 如果当前分布属性发生变化

                                if (VueThis.CurHistogramAttr !== thisNodeName) {
                                    VueThis.CurHistogramAttr = thisNodeName;
                                    if (!VueThis.AttrSensitive[thisNodeName]) {
                                        VueThis.updateAttrHistogram(thisNodeName).then(
                                            (simulateData) => {
                                                VueThis.simulateDataRecord[thisNodeName] = simulateData;
                                                VueThis.updateSimulatedAttrLineChart(
                                                    thisNodeName,
                                                    simulateData
                                                );
                                            }
                                        );
                                    } else {
                                        // 敏感属性的情况
                                        if (VueThis.simulateDataRecord[thisNodeName]) {
                                            VueThis.updateAttrHistogram(
                                                thisNodeName,
                                                VueThis.simulateDataRecord[thisNodeName]
                                            );

                                            VueThis.updateSimulatedAttrLineChart(
                                                thisNodeName,
                                                VueThis.simulateDataRecord[thisNodeName]
                                            );
                                        } else {
                                            let simulateData = {};
                                            let binRange = VueThis.AttrBinRangeMap[thisNodeName];
                                            let baseVal =
                                                VueThis.CurExDataset.length / (binRange.length - 1);
                                            for (let i in binRange) {
                                                let idx = +i;
                                                if (idx !== 0) {
                                                    let noise = (Math.random() * baseVal) / 2;
                                                    simulateData[
                                                    binRange[idx - 1] + "-" + binRange[idx]
                                                        ] = baseVal + noise;
                                                }
                                            }
                                            VueThis.simulateDataRecord[thisNodeName] = simulateData;
                                            VueThis.SensitiveAttrSimulate[thisNodeName] =
                                                simulateData;
                                            VueThis.updateAttrHistogram(thisNodeName, simulateData);
                                            VueThis.updateSimulatedAttrLineChart(
                                                thisNodeName,
                                                simulateData
                                            );
                                        }
                                    }
                                }

                                // 移动连线
                                d3.selectAll(".ContactedAttr").each(function () {
                                    let thatNode = this;
                                    let thatNodeName = d3.select(thatNode).attr("name");
                                    let NodeNameList = [thisNodeName, thatNodeName].sort();
                                    let lineName = `${NodeNameList[0]}±${NodeNameList[1]}`;
                                    let isSensitiveQuery =
                                        VueThis.AttrSensitive[NodeNameList[0]] ||
                                        VueThis.AttrSensitive[NodeNameList[1]];
                                    const Line = LineContainer.select(`#${lineName}`);

                                    let [x1, y1] = d3
                                        .select(thisNode)
                                        .attr("transform")
                                        .match(/-?[\d.]+/g);
                                    let [x2, y2] = d3
                                        .select(thatNode)
                                        .attr("transform")
                                        .match(/-?[\d.]+/g);
                                    let [rectW1, rectH1] = VueThis.rectWHMap[thisNodeName];
                                    let [rectW2, rectH2] = VueThis.rectWHMap[thatNodeName];
                                    x1 = +x1 + rectW1 / 2 + 15;
                                    y1 = +y1 + rectH1 / 2 + 30;
                                    x2 = +x2 + rectW2 / 2 + 15;
                                    y2 = +y2 + rectH2 / 2 + 30;
                                    Line.attr("x1", x1)
                                        .attr("y1", y1)
                                        .attr("x2", x2)
                                        .attr("y2", y2);

                                    // if (isSensitiveQuery) {
                                    const text = LineContainer.select(`#${lineName}text`);
                                    text.attr("x", (x1 + x2) / 2).attr("y", (y1 + y2) / 2 + 5);
                                    // }
                                });
                            }
                            d3.select(thisNode).classed("ContactedAttr", true);
                        } else {
                            d3.select(this).attr("ContactedAttr", false);
                            // 移除连线
                        }
                    })
                    .on("end", function (event) {
                        d3.select(this).classed("active", false);
                    })
            );

            let QueryResultChart = d3.select("#QueryResultChart");
            this.SvgWidth = parseInt(QueryResultChart.style("width"));
            this.SvgHeight = parseInt(QueryResultChart.style("height"));
            console.log(this.SvgWidth, this.SvgHeight);
        },
        resetDatabase() {
            // 读数据
            this.readData().then(() => {
                this.setMoveNodeEvent();
            });
        },
    },
    created() {
        this.resetDatabase();
    },

    mounted() {

    },
};
</script>

<style scoped>
/* base style start */
svg text {
    font-size: 16px;
}

.ColorBox {
    background-color: #fff;
}

.FlexRow {
    display: flex;
    flex-direction: row;
}

/* .FlexSpaceBetween {
  justify-content: space-between;
} */

.MainHeading {
    font-size: 20px;
    margin-bottom: 5px;
    padding: 5px 0 0 5px;
}

.SubHeading {
    font-size: 18px;
    margin: 5px 0 5px 5px;
}

.SubSubHeading {
    font-size: 16px;
    margin: 5px 0 5px 5px;
}

.MainText,
span {
    font-size: 16px;
    line-height: 32px;
}
/* base style end */

/* base frame start */
.LeftPart,
.MidPart,
.RightPart {
    margin: 10px;
    height: calc(100% - 20px);
}
.LeftPart {
    margin-right: 5px;
    width: calc(30% - 5px);

    display: flex;
    flex-direction: column;
}
.MidPart {
    width: calc(20%);
    margin-right: 5px;
    margin-left: 5px;
}

.RightPart {
    margin-left: 5px;
    width: calc(50% - 5px);
}
/* base frame end */

/* LeftPart style start */
.BaseMessPart {
    height: calc(5% - 10px);
    margin-bottom: 5px;
}
.QueryInputPart {
    height: calc(95%);
    margin: 5px 0 0 0;
    position: relative;
}
.DBAttrBody {
    height: calc(100% - 30px);
    width: 100%;
    position: relative;
    top: -30px;
}
.SingleAttrQuery {
    stroke: aqua;
}
/* LeftPart style end */

/* RightPart style start */
.VisPart {
    height: 100%;
}
.QueryStrategyBody {
    height: calc(70% - 10px);
    margin-top: 10px;
    width: 100%;
    display: flex;
    flex-direction: column;
}
.QueryStrategyItem {
    width: 350px;
    /* height: 350px; */
    text-align: center;
    margin: 10px 10px;
}
.CurStrategyQuery {
    background-color: rgba(52, 152, 219, 0.5) !important;
}

.ChartPart {
    height: 100%;
    display: flex;
    flex-direction: row;
}

.MainChart {
    height: 100%;
    width: calc(100% - 10px);
    margin-right: 10px;
    position: relative;
}
#QueryResultChart {
    height: calc(100% - 30px);
    width: 100%;
}

.AdjustPanel {
    height: 100%;
    width: 30%;
    border: #555 solid 4px;
}

.QueryTemplatePart {
    width: 100%;
    height: 100%;
}

.QueryGranularityAdjust {
    width: 100%;
    justify-content: space-between;
    margin-top: 0;
    align-items: center;
    padding: 0 2%;
}

.QuerySimulationModal {
    width: 100px;
    height: 40px;
    line-height: 34px;
    border: 3px solid #555;
    margin: 5px;
    text-align: center;
}

.CurModal {
    border-color: aqua;
}

/* RightPart style end */

/* tobe sorted */
.CorrInputGroup {
    position: absolute;
    left: 20px;
    top: 290px;
}
.ResetButton {
    position: absolute;
    bottom: 295px;
    right: 33px;
}

.QueryStrategyItemSvg {
    height: 100%;
    width: 150px;
}

.AttrBinRangeSlider {
    width: 200px !important;
}
.CurQueryEpsilonInput {
    width: 50px;
}
.QueryTemplatePart {
    position: relative;
}
.QueryTemplateTop {
    height: 35%;
}

.QueryTemplateBottom {
    height: 100%;
}

.TextDivider {
    margin: 0;
    border-color: #aaa;
    margin: 0 10px;
    width: calc(100% - 20px);
}
.SubmitRow {
    text-align: center;
    position: absolute;
    top: calc(31% + 5px);
    left: 7%;
    width: 80%;
}
.AttrFilterPanel {
    position: absolute;
    top: 50px;
    left: 10px;
    /* display: flex; */
}

.histogramAttr {
    stroke-width: 7px;
}

.NosieModeChange {
    align-items: center;
}

.tickSvg {
    width: 225px;
    height: 70px;
}

.SimulateState {
    background-color: rgb(176, 176, 176);
    border: rgb(176, 176, 176);
}

.IssueState {
    background-color: rgb(176, 176, 176);
    border: rgb(176, 176, 176);
}

.QueryStrategyItem .blueBg {
    background-color: rgba(52, 152, 219, 0.2);
    /* flex: 1; */
    cursor: pointer;
}

.QueryStrategyItem .blueBg:not(:first-child) {
    margin-top: 10px;
}

.queryScroll {
    flex: 1;
    height: 150px;
}

.svgpart svg {
    height: 55px;
    width: 55px;
}

.textpart {
    padding-left: 10px;
    padding-top: 5px;
    flex: 1;
    text-align: start;
}

.textpart div{
    line-height: 1.3em;
}

.greySvgText {
    fill: #666;
}

.ExplorationProgress {
    position: absolute;
    left: 280px;
    top: 245px;
    font-size: 14px !important;
    /*width: 100px;*/
}
.ExplorationProgressSlider {
    margin-left: 20px;
}

</style>


<style>
/* .el-button--primary,
.el-switch__core {
  background-color: rgba(52, 152, 219, 1) !important;
  border-color: rgba(52, 152, 219, 1) !important;
} */
.legendMText {
    fill: #666;
    font-size: 14px !important;
}

.legendText,
.tick > text {
    font-size: 12px !important;
}

.el-switch__label {
    color: #666;
}

.el-switch__label * {
    font-size: 16px !important;
}

.el-switch__label.is-active {
    color: rgba(52, 152, 219, 1) !important;
}

.queryScroll .el-scrollbar__view {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.svg_sensitive_attr {
    fill: rgb(234,120,119);
}

.svg_Nonsensitive_attr {
    fill: rgba(52, 152, 219,1.0);
}

.ExplorationProgress div {
    font-size: 14px !important;
}
</style>