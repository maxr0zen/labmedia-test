<template>
  <div class="charts-section">
    <div class="chart-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-btn"
        :class="{ active: activeChart === tab.key }"
        @click="activeChart = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>
    <div class="chart-card">
      <v-chart class="chart" :option="currentChartOption" autoresize />
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart, LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  DataZoomComponent,
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
  DataZoomComponent,
])

const props = defineProps({
  clients: { type: Array, default: () => [] },
  payments: { type: Array, default: () => [] },
})

const activeChart = ref('timeline')

const tabs = [
  { key: 'timeline', label: 'Динамика платежей' },
  { key: 'country', label: 'По странам' },
  { key: 'topPayers', label: 'Топ плательщиков' },
  { key: 'distribution', label: 'Распределение' },
]

const countryData = computed(() => {
  const map = {}
  props.payments.forEach((p) => {
    const country = p.payer_details?.country || 'Неизвестно'
    map[country] = (map[country] || 0) + Number(p.amount)
  })
  return Object.entries(map).map(([name, value]) => ({ name, value: Number(value.toFixed(2)) }))
})

const countryChartOption = computed(() => ({
  tooltip: {
    trigger: 'item',
    formatter: (params) => `${params.name}: $${params.value.toLocaleString()} (${params.percent}%)`,
    backgroundColor: 'rgba(255,255,255,0.95)',
    borderColor: '#ddd',
    textStyle: { color: '#333' },
  },
  legend: { bottom: 0, left: 'center', textStyle: { color: '#555' } },
  series: [{
    type: 'pie',
    radius: ['45%', '75%'],
    center: ['50%', '45%'],
    avoidLabelOverlap: true,
    itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 3 },
    label: { show: true, formatter: '{b}\n{d}%', color: '#555' },
    emphasis: {
      label: { show: true, fontSize: 18, fontWeight: 'bold' },
      itemStyle: { shadowBlur: 20, shadowColor: 'rgba(0,0,0,0.25)' },
    },
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
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(255,255,255,0.95)',
    borderColor: '#ddd',
    textStyle: { color: '#333' },
    formatter: (params) => {
      const p = params[0]
      return `<strong>${p.name}</strong><br/>Сумма: $${Number(p.value).toLocaleString()}`
    },
  },
  grid: { left: '3%', right: '4%', bottom: '15%', top: '10%', containLabel: true },
  dataZoom: [{ type: 'inside' }, { type: 'slider', bottom: 10 }],
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: timelineData.value.dates,
    axisLine: { lineStyle: { color: '#999' } },
    axisLabel: { color: '#555' },
  },
  yAxis: {
    type: 'value',
    axisLabel: { formatter: '${value}', color: '#555' },
    splitLine: { lineStyle: { color: '#eee' } },
  },
  series: [{
    name: 'Сумма',
    type: 'line',
    smooth: true,
    symbol: 'circle',
    symbolSize: 8,
    lineStyle: { width: 3, color: '#1a237e' },
    areaStyle: {
      color: {
        type: 'linear',
        x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [
          { offset: 0, color: 'rgba(26, 35, 126, 0.4)' },
          { offset: 1, color: 'rgba(26, 35, 126, 0.02)' },
        ],
      },
    },
    itemStyle: { color: '#1a237e', borderColor: '#fff', borderWidth: 2 },
    emphasis: {
      focus: 'series',
      itemStyle: { shadowBlur: 15, shadowColor: 'rgba(26,35,126,0.5)' },
    },
    data: timelineData.value.values,
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
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' },
    backgroundColor: 'rgba(255,255,255,0.95)',
    borderColor: '#ddd',
    textStyle: { color: '#333' },
    formatter: (params) => {
      const p = params[0]
      return `<strong>${p.name}</strong><br/>Всего: $${Number(p.value).toLocaleString()}`
    },
  },
  grid: { left: '3%', right: '8%', bottom: '3%', top: '5%', containLabel: true },
  xAxis: {
    type: 'value',
    axisLabel: { formatter: '${value}', color: '#555' },
    splitLine: { lineStyle: { color: '#eee' } },
  },
  yAxis: {
    type: 'category',
    data: topPayers.value.map(([name]) => name).reverse(),
    axisLine: { lineStyle: { color: '#999' } },
    axisLabel: { color: '#555' },
  },
  series: [{
    name: 'Всего',
    type: 'bar',
    data: topPayers.value.map(([, v]) => Number(v.toFixed(2))).reverse(),
    itemStyle: {
      color: {
        type: 'linear',
        x: 0, y: 0, x2: 1, y2: 0,
        colorStops: [
          { offset: 0, color: '#3949ab' },
          { offset: 1, color: '#1a237e' },
        ],
      },
      borderRadius: [0, 8, 8, 0],
    },
    emphasis: {
      itemStyle: { shadowBlur: 15, shadowColor: 'rgba(57,73,171,0.5)' },
    },
    barWidth: '60%',
  }],
}))

const distributionData = computed(() => {
  const ranges = {
    '$0–100': 0,
    '$100–500': 0,
    '$500–1000': 0,
    '$1000–5000': 0,
    '$5000+': 0,
  }
  props.payments.forEach((p) => {
    const amt = Number(p.amount)
    if (amt <= 100) ranges['$0–100']++
    else if (amt <= 500) ranges['$100–500']++
    else if (amt <= 1000) ranges['$500–1000']++
    else if (amt <= 5000) ranges['$1000–5000']++
    else ranges['$5000+']++
  })
  return Object.entries(ranges).map(([name, value]) => ({ name, value }))
})

const distributionOption = computed(() => ({
  tooltip: {
    trigger: 'item',
    backgroundColor: 'rgba(255,255,255,0.95)',
    borderColor: '#ddd',
    textStyle: { color: '#333' },
    formatter: (params) => `${params.name}: <strong>${params.value}</strong> платежей`,
  },
  legend: { bottom: 0, left: 'center', textStyle: { color: '#555' } },
  series: [{
    type: 'pie',
    radius: '65%',
    center: ['50%', '45%'],
    data: distributionData.value,
    itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
    emphasis: {
      itemStyle: { shadowBlur: 20, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.3)' },
      label: { show: true, fontSize: 16, fontWeight: 'bold' },
    },
    label: { show: true, formatter: '{b}\n{c} шт.', color: '#555' },
  }],
}))

const currentChartOption = computed(() => {
  switch (activeChart.value) {
    case 'country': return countryChartOption.value
    case 'topPayers': return topPayersOption.value
    case 'distribution': return distributionOption.value
    default: return timelineChartOption.value
  }
})
</script>

<style scoped>
.charts-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chart-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 20px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  color: #555;
  transition: all 0.2s;
}

.tab-btn:hover {
  border-color: #1a237e;
  color: #1a237e;
}

.tab-btn.active {
  background: #1a237e;
  color: white;
  border-color: #1a237e;
  box-shadow: 0 4px 12px rgba(26, 35, 126, 0.25);
}

.chart-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  padding: 24px;
}

.chart {
  width: 100%;
  height: 520px;
}
</style>
