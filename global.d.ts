declare var $$inject: {
    log: any;
    notify: {
        info: ()=> void;
        warn: ()=> void;
        error: ()=> void;
        success: ()=> void;
        toast: ()=> void;
    };
    result: any;
    properties: {
        authToken: string;
        config: any;
        document: {
            id: number;
            hash: string;
            databaseId: number;
            archiveId: number;
            fileId: string;
        };
    };
    utility: {
        newGuid: () => string;
    };
    tableFields: any;
    fields: any;
    setPendingChanges: () => void;
    save: ()=> void;
};