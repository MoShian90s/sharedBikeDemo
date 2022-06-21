<template>
<div>
    <el-row :gutter="50" type="flex" justify="flex-start" style="flex-wrap:wrap">
        <el-col :xs='16' :sm='16' :md='16' :lg='16' :xl='16' class="visualCards">
            <div>
                <GmapMap
                    :center="{lat:10, lng:10}"
                    :zoom="7"
                    map-type-id="terrain"
                    style="width: 100%; height: 80vh; box-shadow: 0 3px 5px rgba(0, 0, 0, .12), 0 0 8px rgba(0, 0, 0, .1)" ref="mapRef" id="mapRef">
                </GmapMap>
            </div>
        </el-col>
        <el-col :xs='8' :sm='8' :md='8' :lg='8' :xl='8' class="visualCards">
            <el-card class='box-card' shadow='always' body-style="padding:5% 10% 5% 10%">
                <h4>Bike Locations Distribution During the Defined Time</h4>
                <el-form>
                    <el-form-item>
                        <el-select v-model="type" style="width:100%;margin-top:5%">
                            <el-option label="🎨 HeatMap" value="heatmap"></el-option>
                            <el-option label="🎯 Marker" value="marker"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-date-picker
                            v-model="DefinedTime"
                            type="datetimerange"
                            range-separator="To"
                            start-placeholder="Start Time"
                            end-placeholder="End Time"
                            value-format="yyyy-MM-dd HH:mm:ss"
                            style="width:100%">
                        </el-date-picker>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-col>
    </el-row>
</div>
</template>

<script>
import { gmapApi } from 'gmap-vue'
import axios from 'axios'
import Vue from 'vue'
import qs from 'qs'

export default {
    data(){
        return{
            map:null,
            heatmap:null,
            getPoints:[],
            markersArray:[],
            DefinedTime:['2021-01-01 00:00:00','2022-01-01 00:00:00'],
            type:'',
        }
    },
    computed:{
        google: gmapApi,
        bikes:function(){
            return bikes.data
        }
    },
    watch:{
        type:async function(){
            let that=this
            await this.dataRefresher()
            if(that.type==='heatmap'){
                this.HeatMapSet(this.map,this.getPoints,40)
                while(that.markersArray.length){
                    that.markersArray.pop().setMap(null)
                }
            }else{
                this.MarkerSet(this.map,this.bikes)
                this.heatmap.setMap(null)
            }
        },
        DefinedTime:async function(){
            let that=this
            if(that.type==='heatmap'){
                that.heatmap.setMap(null)
                await that.dataRefresher()
                that.HeatMapSet(that.map,that.getPoints,40)
            }else{
                while(that.markersArray.length){
                    that.markersArray.pop().setMap(null)
                }
                await that.dataRefresher()
                that.MarkerSet(that.map,that.bikes)
            }
        }
    },
    async mounted () {
        let that=this;
        
        //initialization
        that.markersArray=new Array;
        await that.$gmapApiPromiseLazy().then(()=>{
            that.Init()
        })
    },
    methods:{
        async dataRefresher(){
            let that=this;
            let google=that.google
            let payload=qs.stringify({start:that.DefinedTime[0],end:that.DefinedTime[1]})
            await axios.post(that.$baseURL+'/manager/get_condition_bike/',payload)
                .then(function(response) {
                    let data=[];
                    response.data.forEach(element => {
                        let item={}
                        item['latitude']=element['Start_location_latitude']
                        item['longitude']=element['Start_location_longitude']
                        data.push(item)
                    });
                    bikes.data=data;

                    //store this.getPoints
                    that.getPoints=[]
                    
                    for(var i=0;i<that.bikes.length;i++){
                        var bikeloc = new google.maps.LatLng((that.bikes)[i]['latitude'], that.bikes[i]['longitude'])
                        that.getPoints.push(bikeloc)
                    }
                })
                .catch(function (error) {
                    console.log(error);
            });
        },
        HeatMapSet(map, getPoints, radius){
            let that=this
            let google=this.google
            that.heatmap = new google.maps.visualization.HeatmapLayer({
                data: getPoints,
                map: map,
            })
            that.heatmap.setMap(that.heatmap.getMap() ? map : null);
            that.HeatMapRadiusChange(that.heatmap, radius)
            that.heatmap.set("opacity", that.heatmap.get("opacity") ? null : 0.4);
        },
        HeatMapRadiusChange(heatmap,radius){
            heatmap.set("radius",heatmap.get('radius')?null:radius)
        },
        MarkerSet(map,bikes){
            let that=this
            for(let i=0;i<bikes.length;i++){
                that.EachMarkerset(bikes[i],map)
            }
        },
        EachMarkerset(eachbike, map){
            let that=this;
            let google=that.google;

            // Add the marker at the clicked location, and add the next-available label
            // from the array of alphabetical characters.
            var bikeloc = new google.maps.LatLng(eachbike['latitude'], eachbike['longitude']);
            let marker = new google.maps.Marker({
                position: bikeloc,
                map: map,
                icon: ''
            });
            that.markersArray.push(marker);

            var infowindow = new google.maps.InfoWindow({
                content: 'ID: ' + String(eachbike.id) + '<br>' +
                    'Insurance: ' + String(eachbike.Insurance_id) + '<br>' +
                    'Brand: ' + String(eachbike.Brand) + '<br>'
            });
            marker.addListener("click", () => {
                infowindow.open(map, marker);
                console.log('move')
            });
        },
        Init(){
            let that=this
            let google=that.google;
            
            //init
            var mapProp = {
                center: new google.maps.LatLng(55.835, -4.277),
                zoom: 13,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            //store this.map
            that.$refs.mapRef.$mapPromise.then((map) => {
                that.map = map;
                that.map.setOptions(mapProp);
            })
            that.dataRefresher()
            //set heatmap
            that.HeatMapSet(that.map,that.getPoints,40)
        }
    },
}

export var bikes=Vue.observable({data:[]})
</script>