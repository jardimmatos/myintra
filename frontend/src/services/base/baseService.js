import ConfigService from '../index'
class BaseService extends ConfigService {
    constructor(){
        super('base/api/v1/')
    }
    async get_monitor_status(){
        return await this.get('monitor/monitors/')
    }
}
export default BaseService
