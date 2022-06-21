<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">home</el-breadcrumb-item>
      <el-breadcrumb-item>Maintenance information</el-breadcrumb-item>
      <el-breadcrumb-item>Your order</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-table :data="tempList" border stripe>
        <el-table-column label="ID" prop="ID" width="120px"></el-table-column>
        <el-table-column label="Bike ID" prop="Bike_id" width="120px"></el-table-column>
        <el-table-column label="Repair Status" prop="Repair_status" width="120px"></el-table-column>
        <!-- <el-table-column label="Address" prop="address" width="120px"></el-table-column> -->
        <!-- <el-table-column fixed="right" label="options" width="100">
          <template slot-scope="scope">
            <el-button v-show="scope.row.Repair_status=='under repair'" @click="handleClick(scope.row)" type="text" size="small">finish</el-button>
          </template>
        </el-table-column> -->
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
        Operator_id: 0,
        currentPage: 1,
        totalnumber: 0,
        pageSize: 5,
        tempList: [],
        repairData: [],
        total: 1
      }
    },
    methods: {
      handleSizeChange(val) {
        this.pageSize = val;
        this.handleCurrentChange(this.currentPage);
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.currentChangePage(this.repairData, this.currentPage)
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
        console.log(this.tempList)
      }
    },
    created() {
      let that = this
      this.Operator_id = this.$session.get("Operator_id")
      console.log(this.Operator_id)
      this.$axios.get(this.$baseURL+'/operator/' + this.Operator_id + '/repairhistory/').then(function(res) {
        console.log(res)
        for (var i = 0; i < res.data.length; i++) {
          that.repairData.push({
            "ID":res.data[i].pk,
            "Bike_id": res.data[i].fields.Bike_id,
            "Repair_status":"repaired",
          })
        }
        console.log(that.repairData)
        that.$data.totalnumber = that.$data.repairData.length;
        that.currentChangePage(that.repairData, 1);
      }).catch(function(error) {
        console.log(error);
      })
    }
  }
</script>
<style scoped>
.el-card{
	box-shadow: 0 1px 1px rgba(0,0,0,0.15) !important;
}
</style>
