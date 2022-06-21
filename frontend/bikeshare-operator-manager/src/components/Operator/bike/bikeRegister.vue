<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">home</el-breadcrumb-item>
      <el-breadcrumb-item>Bike information</el-breadcrumb-item>
      <el-breadcrumb-item>Bike Register</el-breadcrumb-item>
    </el-breadcrumb>
    <el-form ref="form" :model="form" label-width="60px">
      <el-form-item label="Brand" prop="brand" label-width="120px">
        <el-select v-model="form.brand" filterable clearable placeholder="">
          <el-option v-for="item in brands" :key="item.value" :label="item.value" :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Insurance ID" prop="insurance_id" label-width="120px">
        <el-input v-model="form.insurance_id" width="120px"></el-input>
      </el-form-item>
      <el-form-item label="location" prop="location" label-width="120px">
        <el-button type="primary" @click="chooseLocation">choose a location</el-button>
        <legend class="lt">&nbsp;lat:</legend>
        <el-input v-model="form.lat" width="120px"></el-input>
        <legend class="lt">&nbsp;lng:</legend>
        <el-input v-model="form.lng" width="120px"></el-input>

      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Register</el-button>
      </el-form-item>
    </el-form>
<div ref="googleMap" id="googleMap" style="width:auto;height:600px;"></div>
  </div>
</template>

<script>
  import qs from 'qs'
  export default {
    data() {
      return {
        form: {
          brand:'',
          insurance_id: '',
          lat: '',
          lng: ''
        },
        brands:[{
          value:"Raleigh"
        },{
          value:"Focus"
        },{
          value:"Felt"
        },{
          value:"Specialized"
        },{
          value:"Trek"
        },{
          value:"Pinarello"
        },{
          value:"Eddy Merchx"
        },{
          value:"BMC"
        },{
          value:"Giant"
        },{
          value:"GT"
        }]
      }
    },
    mounted() {
      let that=this
      var mapProp = {
                center: new google.maps.LatLng(55.835, -4.277),
                zoom: 13,
                mapTypeId: google.maps.MapTypeId.ROADMAP
              };
      this.map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
    },
    methods: {
      async onSubmit() {
        let that = this
        var fdata = qs.stringify({
          "brand": this.form.brand,
          "insurance_id": this.form.insurance_id,
          "latitude": this.form.lat,
          "longitude": this.form.lng
        })
        await this.$axios
          .post(this.$baseURL + '/operator/registerbike/', fdata)
          .then(function(result) {
            console.log(result);
            that.$message.info(result.data);
            that.form.brand = ''
            that.form.insurance_id = ''
            that.form.lat = ''
            that.form.lng = ''
          }).catch(function(err) {
            console.log(err);
          })
      },
      chooseLocation (){
        var map=this.map;
        let that=this
        const clickmarker = new google.maps.Marker({
          draggable: true,
          icon: "http://maps.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png",
          animation: google.maps.Animation.DROP,
        });
        //----------click the map to put a marker----------//
        google.maps.event.addListener(map, "click", (event) => {
          clickmarker.setPosition(event.latLng); //return the location to the Marker
          that.form.lat=clickmarker.getPosition().lat();
          that.form.lng=clickmarker.getPosition().lng();
          clickmarker.setMap(map);
        });

        clickmarker.addListener('click', toggleBounce);
        clickmarker.addListener('dragend', dragendfunc);

        //----------get marker's animation---------//
        function toggleBounce() {
          if (clickmarker.getAnimation() !== null) {
            clickmarker.setAnimation(null);
          } else {
            clickmarker.setAnimation(google.maps.Animation.BOUNCE);
          }
        }

        //----------return the exact location----------//
        function dragendfunc() {
          that.form.lng=clickmarker.getPosition().lng();
          that.form.lat=clickmarker.getPosition().lat();
        }
      }
    },
  }
</script>

<style scoped>
.el-card{
	box-shadow: 0 1px 1px rgba(0,0,0,0.15) !important;
}
</style>

