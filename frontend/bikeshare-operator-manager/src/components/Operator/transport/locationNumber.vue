<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">home</el-breadcrumb-item>
      <el-breadcrumb-item>Transport information</el-breadcrumb-item>
      <el-breadcrumb-item>Location information</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <legend class="lt">&nbsp;choose bikes:</legend>
      <el-tag :key="tag" v-for="tag in bikeId" closable :disable-transitions="false" @close="CloseTag(tag)">
        {{tag}}
      </el-tag>
      <br />
      <legend class="lt">&nbsp;choose to location:{{form.tlocation}}<el-button @click="setTlocation()" plain>set a point on the map</el-button></legend>
      <br />
      <el-button type="text" @click="orderShow">create a Transport order</el-button>
    </el-card>
    <br />
    <div ref="googleMap" id="googleMap" style="width:auto;height:600px;"></div>
    <el-dialog title="destirnation" :visible.sync="dialogVisible" width="60%" @close="closeDialog">
      <span slot="footer" class="dialog-footer">
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="Latitude">
            <el-input v-model="form.lat"></el-input>
          </el-form-item>
          <el-form-item label="Longitude">
            <el-input v-model="form.lng"></el-input>
          </el-form-item>
          <el-form-item label="bike Id">
            <el-tag :key="tag" v-for="tag in bikeId" closable :disable-transitions="false" @close="CloseTag(tag)">
              {{tag}}
            </el-tag>
          </el-form-item>
        </el-form>
        <el-button @click="dialogVisible = false">cancel</el-button>
        <el-button type="primary" @click="onSubmit">submit</el-button>
      </span>
    </el-dialog>

  </div>
</template>
<script>
  import MarkLabel from '../../../../MarkLabel.js'
  import qs from 'qs'
  export default {
    data() {
      return {
        bikeId: [],
        total: 1,
        dialogVisible: false,
        form: {
          lat: '',
          lng: '',
          bikeIdList: ''
        },
        bikes: [],
        Operator_id:0
      }
    },
    mounted() {
      this.initialize()
    },
    methods: {
      orderShow() {
        this.$data.dialogVisible = true
        this.$data.form.bikeIdList = this.$data.bikeId
      },
      CloseTag(tag) {
        this.bikeId.splice(this.bikeId.indexOf(tag), 1);
        console.log(tag);
      },
      setTlocation() {
        var map=this.map;
        let that=this
        const clickmarker = new google.maps.Marker({
          draggable: true, //marker 设为可拖动
          animation: google.maps.Animation.DROP, //动画属性设为DROP
        });
        //----------单击地图放置一个Marker----------//
        google.maps.event.addListener(map, "click", (event) => {
          clickmarker.setPosition(event.latLng); //将点击坐标赋值给Marker
          console.log(clickmarker.getPosition().lat(), clickmarker.getPosition().lng()); //后台输出经纬度
          that.form.lat=clickmarker.getPosition().lat();
          that.form.lng=clickmarker.getPosition().lng();
          clickmarker.setMap(map); //设置的Marker在地图中生效
          //clickmarker.setMap(null);//这行语句可以删除Marker，如果需要这个功能可以自行绑定一个Button
        });

        clickmarker.addListener('click', toggleBounce); //鼠标左键按住Marker可以拖动
        clickmarker.addListener('dragend', dragendfunc); //鼠标左键松开之后返回Marker坐标

        //----------单击Marker可以让它在地图上有一个跳动动画，再次单击取消跳动，娱乐功能----------//
        function toggleBounce() {
          if (clickmarker.getAnimation() !== null) {
            clickmarker.setAnimation(null);
          } else {
            clickmarker.setAnimation(google.maps.Animation.BOUNCE);
          }
        }

        //----------鼠标左键松开之后返回Marker坐标----------//
        function dragendfunc() {
          console.log(clickmarker.getPosition().lat(), clickmarker.getPosition().lng()); //后台输出经纬度
          that.form.lng=clickmarker.getPosition().lng();
          that.form.lat=clickmarker.getPosition().lat();
        }
      },
      onSubmit() {
        this.$data.dialogVisible = false
        let that=this
        let bikeidd=JSON.stringify(that.bikeId)
        this.Operator_id=this.$session.get("Operator_id")
        console.log(bikeidd)
        var fdata=qs.stringify({"operator_id":this.Operator_id,"bike_ids":(that.bikeId),"latitude":that.form.lat,"longitude":that.form.lng},{ indices: false })
        this.$axios.post(this.$baseURL+'/operator/movebikes/',fdata)
        .then(function(res){
          console.log("succeed");
          that.bikeId=[]
          that.bikeIdList=''
		  that.$message.success(res.data)
        }).catch(function(error){
          console.log(error);
        })
        this.initialize()
      },
      closeDialog() {
        this.$data.form.bikeIdList = ''
        console.log(this.$data.form)
      },
      pushId(Selectedinfo) {
        this.$data.bikeId.push(parseInt(Selectedinfo.ID));
      },
      showposition() {
        var map=this.map;
        for (var i = 0; i < this.$data.bikes.length; i++) {
          var eachbike = this.$data.bikes[i]
          this.addMarker(eachbike, this.map)
        }
      },
      addMarker(eachbike, map) {
        // Add the marker at the clicked location, and add the next-available label
        // from the array of alphabetical characters.
        let that = this;
        var bikeloc = new google.maps.LatLng(eachbike.Home_location_lat, eachbike.Home_location_long);
        var image = 'http://maps.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png';
        const marker = new google.maps.MarkerWithLabel({
          position: bikeloc,
          map: map,
          icon: image,
          labelContent: String(eachbike.ID),
          labelAnchor: new google.maps.Point(10, 50),
          labelClass: "",
          labelStyle: {
            fontSize: "10px",
            lineHeight: "14px",
            padding: "2px",
            backgroundColor: 'gray',
            color: 'white'
          }
        });
        var infowindow = new google.maps.InfoWindow({
          content: "ID:" + eachbike.ID + '<br />' + "Lat:" + eachbike.Home_location_lat + '<br />' + "Lon:" +
            eachbike.Home_location_long
        });
        infowindow.addListener("closeclick", () => {
          console.log(Selectedinfo);
          that.$data.bikeId.some((item, i) => {
            if (item == Selectedinfo.ID) {
              that.$data.bikeId.splice(i, 1);
              return true;
            }
          })
        })
        /*选中单车的信息*/
        var Selectedinfo = {
          ID: String(eachbike.ID),
          Lat: String(eachbike.Home_location_lat),
          Lon: String(eachbike.Home_location_long)
        }
        /**/
        marker.addListener("click", () => {
          var flag=false;
          infowindow.open(map, marker); //显示已选中
          console.log(Selectedinfo); //控制台输出选中单车的信息
          for(var i = 0;i<that.bikeId.length;i++){
            if(that.bikeId[i]==Selectedinfo.ID){
              flag=true;
              break;
            }
          }
          if(!flag){
            that.bikeId.push(parseInt(Selectedinfo.ID));
          }
        });
      },
      initialize() {
        var mapProp = {
          center: new google.maps.LatLng(55.835, -4.277),
          zoom: 13,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        this.map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
        let that = this;
        // this.bikes=[]
        this.$axios.get(this.$baseURL+'/operator/track/').then(function(res) {
          console.log(res.data.length);
          for (var i = 0; i < res.data.length; i++) {
            that.bikes.push({
              ID: res.data[i].pk,
              Home_location_lat: res.data[i].fields.Loc_lat,
              Home_location_long: res.data[i].fields.Loc_long
            })
          }
        }).catch(function(error) {
          console.log(error);
        })
        setTimeout(() => {
          for (var i = 0; i < this.$data.bikes.length; i++) {
            var eachbike = this.$data.bikes[i]
            this.addMarker(eachbike, this.map)
          }
        }, 400);
      }
    }
  }
</script>

<style scoped>
.el-card{
	box-shadow: 0 1px 1px rgba(0,0,0,0.15) !important;
}
</style>
