<template>
  <div class="charts-grid">
    <div class="chart-card">
      <h3>Payments by Country</h3>
      <v-chart class="chart" :option="countryChartOption" autoresize />
    </div>
    <div class="chart-card">
      <h3>Payments Over Time</h3>
      <v-chart class="chart" :option="timelineChartOption" autoresize />
    </div>
    <div class="chart-card">
      <h3>Top Payers</h3>
      <v-chart class="chart" :option="topPayersOption" autoresize />
    </div>
    <div class="chart-card">
      <h3>Payment Distribution</h3>
      <v-chart class="chart" :option="distributionOption" autoresize />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart, LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'

use([
  CanvasRenderer,
  PieChart,
  BarChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
])

const props = defineProps({
  clients: { type: Array, default: () => [] },
  payments: { type: Array, default: () => [] },
})

const countryData = computed(() => {
  const map = {}
  props.payments.forEach((p) => {
    const country = p.payer_details?.country || 'Unknown'
    map[country] = (map[country] || 0) + Number(p.amount)
  })
  return Object.entries(map).map(([name, value]) => ({ name, value: Number(value.toFixed(2)) }))
})

const countryChartOption = computed(() => ({
  tooltip: { trigger: 'item', formatter: '{b}: ${c} ({d}%)' },
  legend: { bottom: 0 },
  series: [{
    type: 'pie',
    radius: ['40%', '70%'],
    avoidLabelOverlap: false,
    itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
    label: { show: false },
    emphasis: { label: { show: true, fontSize: 16, fontWeight: 'bold' } },
    data: countryData.value,
  }],
}))

const timelineData = computed(() => {
  const map = {}
  props.payments.forEach((p) => {
    const date = p.pay_date ? p.pay_date.slice(0, 10) : ''
    if (date) map[date] = (map[date] || 0) + Number(p.amount)
  })
  const sorted = Object.entries(map).sort((a, b) => a[0].localeCompare(b[0]))
  return {
    dates: sorted.map(([d]) => d),
    values: sorted.map(([, v]) => Number(v.toFixed(2))),
  }
})

const timelineChartOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category', boundaryGap: false, data: timelineData.value.dates },
  yAxis: { type: 'value', axisLabel: { formatter: '${value}' } },
  series: [{
    name: 'Amount',
    type: 'line',
    smooth: true,
    areaStyle: { opacity: 0.3 },
    data: timelineData.value.values,
    itemStyle: { color: '#1a237e' },
  }],
}))

const topPayers = computed(() => {
  const map = {}
  props.payments.forEach((p) => {
    const name = p.payer_details ? `${p.payer_details.first_name} ${p.payer_details.last_name}` : `ID ${p.payer}`
    map[name] = (map[name] || 0) + Number(p.amount)
  })
  return Object.entries(map)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
})

const topPayersOption = computed(() => ({
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'value', axisLabel: { formatter: '${value}' } },
  yAxis: { type: 'category', data: topPayers.value.map(([name]) => name).reverse() },
  series: [{
    name: 'Total',
    type: 'bar',
    data: topPayers.value.map(([, v]) => Number(v.toFixed(2))).reverse(),
    itemStyle: { color: '#3949ab', borderRadius: [0, 4, 4, 0] },
  }],
}))

const distributionData = computed(() => {
  const ranges = {
    '0-100': 0,
    '100-500': 0,
    '500-1000': 0,
    '1000-5000': 0,
    '5000+': 0,
  }
  props.payments.forEach((p) => {
    const amt = Number(p.amount)
    if (amt <= 100) ranges['0-100']++
    else if (amt <= 500) ranges['100-500']++
    else if (amt <= 1000) ranges['500-1000']++
    else if (amt <= 5000) ranges['1000-5000']++
    else ranges['5000+']++
  })
  return Object.entries(ranges).map(([name, value]) => ({ name, value }))
})

const distributionOption = computed(() => ({
  tooltip: { trigger: 'item' },
  legend: { bottom: 0 },
  series: [{
    type: 'pie',
    radius: '60%',
    data: distributionData.value,
    emphasis: {
      itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)' },
    },
  }],
}))
</script>

<style scoped>
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
  gap: 20px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 20px;
}

.chart-card h3 {
  margin-bottom: 12px;
  font-size: 1.1rem;
  color: #333;
}

.chart {
  width: 100%;
  height: 320px;
}
</style>
