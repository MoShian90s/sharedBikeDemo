import { shallowMount } from '@vue/test-utils'
import { getBikeids } from '@/components/bike/bikeSearch.vue'
import axios from 'axios'
describe('bikeSearch.vue', () => {
  it('selection return', (done) => {
   axios.get('http://127.0.0.1:8000/operator/track/').then(res => {
      expect(res).toMatchObject({
        status_code:200
      })
      done()
    })
  })
})
