import { defineStore } from 'pinia';

interface ObjectList {
	[key: string]: string[];
}

export const useExamineStore = defineStore('examineModel', {
	state: () => ({
        userIds: [],
        paperId: '',
        isShowUpload: false,
        isShowSelect: false,
    }),
	actions: {
        setIsShowUpload(val: boolean) {
            this.isShowUpload = val
        },
        setIsShowSelect(val: boolean) {
            this.isShowSelect = val
        },
		handleSet(val: string[]) {
			this.key = val;
		},
        setPaperId(id: string) {
            this.paperId = id
        },
        setUserIds(ids: Array<string>) {
            this.userIds = ids;
        }
	}
});
