<template>
<div>
    <el-row :gutter="50" type="flex" justify="center" style="flex-wrap:wrap">
        <el-col :xs='24' :sm='24' :md='24' :lg='24' :xl='24' class="visualCards">
            <el-card class='box-card' shadow='always' body-style="padding:5% 5% 5% 5%">
                <el-row :gutter="50" type="flex" style="flex-wrap:wrap;justify-content:space-around">
                    <el-col :xs='24' :sm='24' :md='8' :lg='8' :xl='8'>
                        <h2>Bike Orders Number Distribution Along the Time Axis</h2>
                        <el-form>
                            <el-form-item>
                                <el-select v-model="grainedLevel" style="width:100%;margin-top:5%">
                                    <el-option label="🔬 Specific Range" value="0"></el-option>
                                    <el-option label="👓 Holistic View" value="1"></el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item>
                                <el-select v-model="type" style="width:100%;">
                                    <el-option label="📅 Day" value="day"></el-option>
                                    <el-option label="📅 Week" value="week"></el-option>
                                    <el-option label="📅 Year" value="year"></el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item v-show="dayVisible">
                                <el-date-picker
                                    v-model="dayRange"
                                    type="date"
                                    placeholder="choose day"
                                    style="width:100%"
                                    @change="definedTimeDay">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item v-show="intervalVisible">
                                <el-select v-model="dayInterval" placeholder="choose the interval" style="width:100%">
                                    <el-option
                                        v-for="item in intervals"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item v-show="dayVisibleChartType">
                                <el-select v-model="chartTypeDaySpecific" style="width:100%;">
                                    <el-option label="📉 Bar" value="bar"></el-option>
                                    <el-option label="🌗 Pie" value="pie"></el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item v-show="weekVisible">
                                <el-date-picker
                                    v-model="weekRange"
                                    type="week"
                                    format="yyyy W week"
                                    placeholder="choose week"
                                    style="width:100%"
                                    @change="definedTimeWeek">
                                </el-date-picker>
                            </el-form-item>
                            <el-form-item v-show="yearVisible">
                                <el-date-picker
                                    v-model="monthRange"
                                    type="monthrange"
                                    range-separator="➡"
                                    start-placeholder="Start Month"
                                    end-placeholder="End Month"
                                    style="width:100%"
                                    @change="definedTimeYear"
                                    value-format="yyyy-MM-dd">
                                </el-date-picker>
                            </el-form-item>
                        </el-form>
                    </el-col>
                    <el-col :xs='24' :sm='24' :md='16' :lg='16' :xl='16' style="display:flex;align-items:center">
                        <div ref="definedTime" style="height:45vh;width:100%;min-height:400px"></div>
                    </el-col>
                </el-row>
            </el-card>
        </el-col>
    </el-row>
</div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'

export default {
    data(){
        return{
            data:[],
            type:'day',
            monthRange:['2021-01-01','2021-12-31'],
            weekRange: new Date(),
            dayRange: new Date(),
            grainedLevel: '1',
            chartTypeDaySpecific:'bar',
            intervals:[{value:'1',label:'⏱ interval 1'},
                        {value:'2',label:'⏱ interval 2'},
                        {value:'6',label:'⏱ interval 6'},
                        {value:'12',label:'⏱ interval 12'}],
            dayInterval:'6',
        }
    },
    watch:{
        type:function(){
            let that=this;
            if(that.type==='day'){
                that.definedTimeDay()
            }else if(that.type==='week'){
                that.definedTimeWeek()
            }else if(that.type==='year'){
                that.definedTimeYear()
            }
        },
        grainedLevel:function(){
            let that=this;
            if(that.type==='day'){
                that.definedTimeDay()
            }else if(that.type==='week'){
                that.definedTimeWeek()
            }else if(that.type==='year'){
                that.definedTimeYear()
            }
        },
        chartTypeDaySpecific:function(){
            this.definedTimeDay()
        },
        dayInterval:function(){
            let that=this;
            if(that.type==='day'){
                that.definedTimeDay()
            }else if(that.type==='week'){
                that.definedTimeWeek()
            }else if(that.type==='year'){
                that.definedTimeYear()
            }
        },
        
    },
    computed:{
        yearVisible:function(){
            if(this.type==='year' && this.grainedLevel==='0'){
                return true;
            }else{
                return false;
            }
        },
        weekVisible:function(){
            if(this.type==='week' && this.grainedLevel==='0'){
                return true;
            }else{
                return false;
            }
        },
        dayVisible:function(){
            if(this.type==='day' && this.grainedLevel==='0'){
                return true;
            }else{
                return false;
            }
        },
        dayVisibleChartType:function(){
            if(this.type==='day'){
                return true;
            }else{
                return false;
            }
        },
        intervalVisible:function(){
            let that=this;
            if(that.type==='day'| that.type==='week'){
                return true
            }else{
                return false
            }
        }
    },
    methods:{
        definedTimeDay(){
            let that=this;

            let day=that.dayRange
            let StartInfo=day.getFullYear().toString()+'-'+(day.getMonth()+1).toString()+'-'+day.getDate().toString()
            let payload=qs.stringify({Day:StartInfo,grainedLevel:that.grainedLevel,intervals:that.dayInterval})
            console.log(payload)
            axios.post(that.$baseURL+'/manager/bike_hours_status/',payload)
                .then(function(response) {
                    let x=[];
                    let y=[];
                    let data=[];
                    response.data['value'].forEach(element => {
                        x.push(element['name'])
                        y.push(element['value'])
                        let item={}
                        item['value']=element['value']
                        item['name']=element['name']
                        data.push(item)
                    });
                    let Chart=that.$echarts.init(that.$refs.definedTime);
                    Chart.clear();
                    let optionBar={
                        tooltip: {
                            trigger: 'item'
                        },
                        legend:{
                            top: '5%',
                            left: 'center',
                        },
                        xAxis:{
                            data:x
                        },
                        yAxis:{},
                        series:[{
                            name:'Defined Time Period',
                            type: 'bar',
                            data:y,
                        }]
                    };
                    let optionPie={
                        tooltip: {
                            trigger: 'item',
                        },
                        legend: {
                            bottom: '5%',
                            left: 'center',
                        },
                        series:[{
                            name: 'Bike Orders',
                            type: 'pie',
                            radius:['40%','70%'],
                            avoidLabelOverlap:false,
                            itemStyle:{
                                borderRadius:10,
                                borderColor:'#fff',
                                borderWidth:2
                            },
                            label:{
                                show:false,
                                position:'center',
                            },
                            emphasis:{
                                label:{
                                    show:true,
                                    fontSize:'40',
                                    fontWeight:'bold'
                                }
                            },
                            labelLine:{
                                show:false
                            },
                            data:data
                        }],
                    }

                    if(that.chartTypeDaySpecific==='bar'){
                        Chart.setOption(optionBar)
                    }else{
                        Chart.setOption(optionPie)
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        definedTimeWeek(){
            let that=this;
            let StartDay=new Date(that.weekRange.getTime()-(that.weekRange.getDay())*24*60*60*1000);
            let StartInfo=StartDay.getFullYear().toString()+'-'+(StartDay.getMonth()+1).toString()+'-'+StartDay.getDate().toString()
            let payload=qs.stringify({StartDay:StartInfo,grainedLevel:that.grainedLevel,intervals:that.dayInterval})

            axios.post(that.$baseURL+'/manager/bike_weeks_status/',payload)
                .then(function(response){
                        let daynames=[]
                        // let intervalnames=[]
                        let days=new Array()
                        for(let index;index<(24/that.dayInterval);index++){
                            days[index]=new Array()
                        }

                        let flag=true
                        response.data.forEach(element => {
                            // names.push(element['name'])
                            let i=0
                            element['value'].forEach(interval=>{
                                if(!flag){
                                    days[i].push(interval['value'])
                                }else{
                                    daynames.push(interval['name'])
                                    days[i]=[]
                                    days[i].push(interval['value'])
                                }
                                i=i+1
                            })
                            flag=false
                        })

                        let Chart=that.$echarts.init(that.$refs.definedTime);
                        Chart.clear(); 
                        let option = {
                            tooltip: {
                                trigger: 'axis',
                                axisPointer: {            // Use axis to trigger tooltip
                                    type: 'shadow'        // 'shadow' as default; can also be 'line' or 'shadow'
                                }
                            },
                            legend: {
                                data: ['0-6','6-12','12-18','18-24']
                            },
                            grid: {
                                left: '3%',
                                right: '4%',
                                bottom: '3%',
                                containLabel: true
                            },
                            xAxis: {
                                type: 'value'
                            },
                            yAxis: {
                                type: 'category',
                                data: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', ]
                            },
                            series: [
                                {
                                    name: '0-6',
                                    type: 'bar',
                                    stack: 'total',
                                    label: {
                                        show: true
                                    },
                                    emphasis: {
                                        focus: 'series'
                                    },
                                    data: ''
                                },
                            ]
                        };
                        let series=[]
                        for(var i=0;i<days.length;i++){
                            let item={}
                            item['name']=daynames[i]
                            item['type']='bar'
                            item['stack']='total'
                            item['label']={show:true}
                            item['emphasis']={focus:'series'}
                            item['data']=days[i]
                            series.push(item)
                        }
                        option['series']=series
                        Chart.setOption(option)
                })
        },
        definedTimeYear(){
            let that=this;
            let payload=null;
            if(that.grainedLevel==='1'){
                payload=qs.stringify({Start_Year:'',Start_Month:'',End_Year:'',End_Month:'',grainedLevel:that.grainedLevel})
            }else{
                let Start=that.monthRange[0].split('-')
                let End=that.monthRange[1].split('-')
                payload=qs.stringify({Start_Year:Start[0],Start_Month:Start[1],End_Year:End[0],End_Month:End[1],grainedLevel:that.grainedLevel})
            }
            axios.post(that.$baseURL+'/manager/bike_years_status/',payload)
                .then(response=>{
                    let x=[]
                    let y=[]
                    response.data.forEach(year => {
                        year['value'].forEach(month=>{
                            x.push(month['name'])
                            y.push(month['value'])
                        })
                    })
                    console.log(x)
                    console.log(y)
                    var colors = ['#5470C6', '#EE6666'];
                    let Chart=that.$echarts.init(that.$refs.definedTime);
                    Chart.clear()
                    let option = {
                        color: colors,

                        tooltip: {
                            trigger: 'none',
                            axisPointer: {
                                type: 'cross'
                            }
                        },
                        legend: {
                            data:['2021']
                        },
                        grid: {
                            top: 70,
                            bottom: 50
                        },
                        xAxis: [
                            {
                                type: 'category',
                                axisTick: {
                                    alignWithLabel: true
                                },
                                axisLine: {
                                    onZero: false,
                                    lineStyle: {
                                        color: colors[1]
                                    }
                                },
                                axisPointer: {
                                    label: {
                                        formatter: function (params) {
                                            return 'Bike Orders  ' + params.value
                                                + (params.seriesData.length ? '：' + params.seriesData[0].data : '');
                                        }
                                    }
                                },
                                data: x
                            },
                        ],
                        yAxis: [
                            {
                                type: 'value'
                            }
                        ],
                        series: [
                            {
                                name: '',
                                type: 'line',
                                smooth: true,
                                emphasis: {
                                    focus: 'series'
                                },
                                data: y
                            }
                        ]
                    };
                    Chart.setOption(option)
                })
        },
    },
    mounted(){
        this.definedTimeDay();
    }
}
</script>

<style scoped>
.visualCards{
    margin: 5vh 0 0 0;
}
</style>