<template>
<div>
    
<GmapMap
    :center="{lat:10, lng:10}"
    :zoom="7"
    map-type-id="terrain"
    style="width: 100%; height: 80vh; box-shadow: 0 3px 5px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .1)" ref="mapRef" id="mapRef">
</GmapMap>

<el-divider class="divider"><i class="el-icon-sort"></i></el-divider>

</div>
</template>

<script>
import { gmapApi } from 'gmap-vue'
import axios from 'axios'
import Vue from 'vue'
import {sharedConfig} from './BikeMapConfig'

export default {
    computed:{
        HeatMapVisbility(){
            return sharedConfig.HeatMapVisbility
        },
        HeatMapRadius(){
            return sharedConfig.HeatMapRadius
        },
        BikeMarkerVisbility(){
            return sharedConfig.BikeMarkerVisbility
        },
        SelfMarkerVisbility(){
            return sharedConfig.SelfMarkerVisbility
        },
        google: gmapApi,
        bikes:function(){
            return bikesData.bikes
        }
    },
    watch:{
        HeatMapVisbility:function(){
            let that=this;
            if(that.HeatMapVisbility===true){
                that.DefineHeatMap(that.map,that.getPoints,that.HeatMapRadius);}
            else{
                that.heatmap.setMap(null);
            }
        },
        HeatMapRadius:function(){
            let that=this;
            if(that.HeatMapVisbility===true){
                that.heatmap.setMap(null);
                that.DefineHeatMap(that.map,that.getPoints,that.HeatMapRadius);}
            else{
                that.heatmap.setMap(null);
            }
        },
        BikeMarkerVisbility:function(){
            let that=this;
            let google=that.google;
            if(that.BikeMarkerVisbility===true){
                that.markersArray=new Array;
                for (var i = 0; i < that.bikes.length; i++) {
                    var bikeloc = new google.maps.LatLng(that.bikes[i].Original_loc_lat, that.bikes[i].Original_loc_long);
                    that.getPoints.push(bikeloc);
                    var eachbike = that.bikes[i];
                    that.addMarker(eachbike, that.map);
                }
            }else if(that.BikeMarkerVisbility===false){
                //why we use while https://stackoverflow.com/questions/26987993/cannot-read-setmap-property-of-undefined-while-using-google-maps-javascript-api
                while(that.markersArray.length){
                    var older=that.markersArray.pop();
                    older.setMap(null);
                }
            }
        },
        SelfMarkerVisbility:function(){
            let that=this;
            if(that.SelfMarkerVisbility===true){
                that.DefineCurLocMarker(that.map);
            }else{
                that.selfMarker.setMap(null);
            }
        }
    },
    data(){
        return{
            map:'',
            selfMarker:'',
            markersArray:[],
            heatmap:'',
            getPoints:'',
            length:'',
        }
    },
    methods: {
        addMarker(eachbike, map) {
            let that=this;
            let google=that.google;

            // Add the marker at the clicked location, and add the next-available label
            // from the array of alphabetical characters.
            var bikeloc = new google.maps.LatLng(eachbike.Original_loc_lat, eachbike.Original_loc_long);
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
        currentlocMarker(pos, map){
            // console.log("currentlocMarker::" + pos);
            let google=this.google;

            this.map.setCenter(pos);
            this.selfMarker = new google.maps.Marker({
              position: pos,
              map: map,
              icon:'http://maps.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png',
            });
        },
        DefineCurLocMarker(map){
            let that=this;
            navigator.geolocation.getCurrentPosition(
                function (position) {
                const pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                    // lat:55.835,
                    // lng:-4.277
                };
                that.currentlocMarker(pos, map);
                },function (error) {//error handler
                    console.log(error)
                }, {//optional attributes
                    enableHighAccuracy: true,//是否要求高精度的地理位置信息
                    timeout: 1000,//对地理位置信息的获取操作做超时限制，如果再该事件内未获取到地理位置信息，将返回错误
                    maximumAge:60*1000//设置缓存有效时间，在该时间段内，获取的地理位置信息还是设置此时间段之前的那次获得的信息，超过这段时间缓存的位置信息会被废弃
                });
        },
        traceroute(Coordinates,map){
            console.log("traceroute::" + Coordinates);
            let google=this.google;

            const flightPath = new google.maps.Polyline({
                path: Coordinates,
                geodesic: true,
                strokeColor: "#0ad4ee",
                strokeOpacity: 1,//线条透明度[0,1]
                strokeWeight:5,//线条宽度
            });
            flightPath.setMap(map);
            this.marker_start = new google.maps.Marker({
                position:  Coordinates[0],
                map: map,
                icon: 'http://www.google.com/mapfiles/dd-start.png'
            });
            this.marker_end = new google.maps.Marker({
                position: Coordinates[Coordinates.length-1],
                map: map,
                icon:'http://www.google.com/mapfiles/dd-end.png'
            });
        },
        toggleHeatmap(heatmap,map) {
            heatmap.setMap(heatmap.getMap() ? map : null);
            // heatmap.setMap(map);
            console.log("toggleHeatmap:: " + heatmap);
        },
        changeGradient(heatmap) {  //changeGradient() modify the solution of paleete
            const gradient = [
              "rgba(0, 255, 255, 0)",
              "rgba(0, 255, 255, 1)",
              "rgba(0, 191, 255, 1)",
              "rgba(0, 127, 255, 1)",
              "rgba(0, 63, 255, 1)",
              "rgba(0, 0, 255, 1)",
              "rgba(0, 0, 223, 1)",
              "rgba(0, 0, 191, 1)",
              "rgba(0, 0, 159, 1)",
              "rgba(0, 0, 127, 1)",
              "rgba(63, 0, 91, 1)",
              "rgba(127, 0, 63, 1)",
              "rgba(191, 0, 31, 1)",
              "rgba(255, 0, 0, 1)",
            ];
            heatmap.set("gradient", heatmap.get("gradient") ? null : gradient);
        },
        changeRadius(heatmap, radius) {
            heatmap.set("radius", heatmap.get("radius") ? null : radius);
        },
        changeOpacity(heatmap) {
            heatmap.set("opacity", heatmap.get("opacity") ? null : 0.4);
        },
        DefineHeatMap(map, getPoints, radius){
            let that=this;
            let google=this.google;
            that.heatmap = new google.maps.visualization.HeatmapLayer({
                data: getPoints,
                map: map,
            });
            that.toggleHeatmap(that.heatmap, that.map);
            that.changeGradient(that.heatmap);
            that.changeRadius(that.heatmap, radius);
            that.changeOpacity(that.heatmap);
        },
        init(){
            let that=this;
            let google=that.google;

            var mapProp = {
                center: new google.maps.LatLng(55.835, -4.277),
                zoom: 13,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            // this.map = new google.maps.Map(document.getElementById("mapRef"), mapProp);
            that.$refs.mapRef.$mapPromise.then((map) => {
                that.map = map;
                that.map.setOptions(mapProp);
            })

            that.getPoints=new Array;
            that.length=that.bikes;
            for (var i = 0; i < that.bikes.length; i++) {
                var bikeloc = new google.maps.LatLng((that.bikes)[i].Original_loc_lat, that.bikes[i].Original_loc_long);
                that.getPoints.push(bikeloc);
                var eachbike = that.bikes[i];
                if(sharedConfig.BikeMarkerVisbility){
                    that.addMarker(eachbike, that.map);
                }
            }
            if(sharedConfig.HeatMapVisbility===true){
                that.DefineHeatMap(that.map,that.getPoints,sharedConfig.HeatMapRadius)
            }
            if(sharedConfig.SelfMarkerVisbility){
                //CurLocMarker
                that.DefineCurLocMarker(that.map);
            }
        },
        dataRefresher(){
            let that=this;
            axios.get(that.$baseURL+'/manager/retrievebikeinfo/')
                .then(function(response) {
                    let data=[];
                    response.data.forEach(element => {
                        let item=element['fields']
                        item['id']=element['pk']
                        data.push(item)
                    });
                    bikesData.bikes=data;
                })
                .catch(function (error) {
                    console.log(error);
            });
        }
    },
    async mounted () {
        let that=this;
        that.dataRefresher();
        //initialization
        that.markersArray=new Array;
        await that.$gmapApiPromiseLazy().then(()=>{
            that.init();
        });
        //AddMarkers
    }
}

var bikesData=Vue.observable({bikes:[]});
</script>

<style scoped>
.divider{
    margin: 7vh 0 7vh 0;
}
</style>
