<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">home</el-breadcrumb-item>
      <el-breadcrumb-item>Transport information</el-breadcrumb-item>
      <el-breadcrumb-item>Your order</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-table :data="tempList" border stripe>
        <el-table-column label="ID" prop="ID" width="60px"></el-table-column>
        <el-table-column label="From location" prop="From_loc" width="180px">
          <template slot-scope="scope">
            <span>lat:</span>{{scope.row.From_loc_lat}}
            <br />
            <span>long:</span>{{scope.row.From_loc_long}}
          </template>
        </el-table-column>
        <el-table-column label="To location" prop="To_loc" width="180px">
          <template slot-scope="scope">
            <span>lat:</span>{{scope.row.To_loc_lat}}
            <br />
            <span>long:</span>{{scope.row.To_loc_long}}
          </template>
        </el-table-column>
        <el-table-column label="number of bikes moved" prop="Number_bikes_moved" width="180px"></el-table-column>
        <el-table-column label="Status" prop="Moving_status" width="120px"></el-table-column>
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
        moveData: [],
        total: 1,
        value: ''
      }
    },
    methods: {
      handleSizeChange(val) {
        this.pageSize = val;
        this.handleCurrentChange(this.currentPage);
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.currentChangePage(this.moveData, this.currentPage)
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
      }
    },
    created() {
      this.moveData = [];
      let that = this
      this.Operator_id=this.$session.get("Operator_id")
      this.$axios.get(this.$baseURL+'/operator/' + this.Operator_id + '/movinghistory/')
        .then(function(res) {
          for (var i = 0; i < res.data.length; i++) {
            that.moveData.push({
              "ID": res.data[i].pk,
              "From_loc_lat": res.data[i].fields.From_loc.split(" ")[0],
              "From_loc_long": res.data[i].fields.From_loc.split(" ")[1],
              "To_loc_lat": res.data[i].fields.To_loc.split(" ")[0],
              "To_loc_long": res.data[i].fields.To_loc.split(" ")[1],
              "Number_bikes_moved": res.data[i].fields.Number_bikes_moved,
              "Moving_status": "moved"
            })
          }
          that.totalnumber = that.moveData.length;
          that.currentChangePage(that.moveData, 1);
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