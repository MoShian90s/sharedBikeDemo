<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">home</el-breadcrumb-item>
      <el-breadcrumb-item>Bike information</el-breadcrumb-item>
      <el-breadcrumb-item>Bike Search</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="4">Bike ID:</el-col>
        <el-col :span="10">
          <el-select v-model="bikeId" filterable clearable placeholder="">
            <el-option v-for="item in bikeids" :key="item.value" :label="item.value" :value="item.value">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="2"></el-col>
        <el-col :span="8">
          <el-button type="primary" @click="showdata">search</el-button>
        </el-col>
      </el-row>
      <el-table :data="tempList" border stripe>
        <el-table-column label="Bike ID" prop="ID" width="120px"></el-table-column>
        <el-table-column label="Insurance ID" prop="Insurance_id" width="120px"></el-table-column>
        <el-table-column label="Brand" prop="Brand" width="120px"></el-table-column>
        <el-table-column label="Location" prop="Home_location_lat,Home_location_long" width="180px">
          <template slot-scope="scope">
            <span>lat:</span>{{scope.row.Home_location_lat}}
            <br />
            <span>long:</span>{{scope.row.Home_location_long}}
          </template>
        </el-table-column>
      </el-table>
      <div>
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
          :page-sizes="[5, 10, 30, 100]" :page-size="pageSize" layout="sizes,jumper" :total="totalnumber">
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        bikeId: '',
        bikeids: [],
        currentPage: 1,
        totalnumber: 0,
        pageSize: 5,
        tempList: [],
        bikeData: []
      }
    },
    mounted() {
      this.getBikeids();
    },
    methods: {
      getBikeids() {
        let that = this
        this.$axios.get(this.$baseURL+'/operator/track/')
          .then(function(res) {
            for (var i = 0; i < res.data.length; i++) {
              that.bikeids.push({
                value: res.data[i].pk
              });
            }
          }).catch(function(error) {
            console.log(error);
          })
      },
      async showdata() {
        let that = this
        if (this.bikeId == "") {
          await this.$axios.get('api/bikesinfo/')
            .then(function(res) {
              that.bikeData = []
              for (var i = 0; i < res.data.length; i++) {
                that.bikeData.push({
                  ID: res.data[i].pk,
                  Insurance_id: res.data[i].fields.Insurance_id,
                  Brand: res.data[i].fields.Brand,
                  Home_location_lat: res.data[i].fields.Original_loc_lat,
                  Home_location_long: res.data[i].fields.Original_loc_long
                })
              }
              that.totalnumber = that.bikeData.length;
              that.currentChangePage(that.bikeData, 1);
            }).catch(function(err) {
              console.log(err)
            })
        } else {
          await this.$axios.get(this.$baseURL+'/' + that.bikeId + '/bikeinfo/')
            .then(function(res) {
              that.bikeData = []
              that.bikeData.push({
                ID: res.data[0].pk,
                Insurance_id: res.data[0].fields.Insurance_id,
                Brand: res.data[0].fields.Brand,
                Home_location_lat: res.data[0].fields.Original_loc_lat,
                Home_location_long: res.data[0].fields.Original_loc_long
              })
              that.totalnumber = that.bikeData.length;
              that.currentChangePage(that.bikeData, 1);
            }).catch(function(error) {
              console.log(error);
            })
        }
      },
      handleSizeChange(val) {
        this.pageSize = val;
        this.handleCurrentChange(this.currentPage);
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.currentChangePage(this.bikeData, this.currentPage)
      },
      currentChangePage(list, currentPage) {
        let from = (currentPage - 1) * this.pageSize;
        let to = currentPage * this.pageSize;
        this.tempList = [];
        for (; from < to; from++) {
          if (list[from]) {
            this.tempList.push(list[from]);
          }
        }
      },
    }
  }
</script>
<style>
  .title {
    font-size: 15px;
    padding-top: 6px;
  }

</style>
<style scoped>
  .el-card{
    box-shadow: 0 1px 1px rgba(0,0,0,0.15) !important;
  }
</style>
