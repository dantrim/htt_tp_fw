parameter EVT_HDR_LWORDS                 = 6;

// EVT_HDR_W1 word description
parameter EVT_HDR_W1_bits                = 64;
parameter EVT_HDR_W1_FLAG_bits           = 8;
parameter EVT_HDR_W1_FLAG_msb            = 63;
parameter EVT_HDR_W1_FLAG_lsb            = 56;
parameter EVT_HDR_W1_FLAG_FLAG           = 171;

parameter EVT_HDR_W1_TRK_TYPE_bits       = 8;
parameter EVT_HDR_W1_TRK_TYPE_msb        = 55;
parameter EVT_HDR_W1_TRK_TYPE_lsb        = 48;
parameter EVT_HDR_W1_TRK_TYPE_RHTT       = 1;
parameter EVT_HDR_W1_TRK_TYPE_GHTT       = 2;

parameter EVT_HDR_W1_SPARE_bits          = 8;
parameter EVT_HDR_W1_SPARE_msb           = 47;
parameter EVT_HDR_W1_SPARE_lsb           = 40;

parameter EVT_HDR_W1_L0ID_bits           = 40;
parameter EVT_HDR_W1_L0ID_msb            = 39;
parameter EVT_HDR_W1_L0ID_lsb            = 0;

// EVT_HDR_W2 word description
parameter EVT_HDR_W2_bits                = 64;
parameter EVT_HDR_W2_BCID_bits           = 12;
parameter EVT_HDR_W2_BCID_msb            = 63;
parameter EVT_HDR_W2_BCID_lsb            = 52;

parameter EVT_HDR_W2_SPARE_bits          = 20;
parameter EVT_HDR_W2_SPARE_msb           = 51;
parameter EVT_HDR_W2_SPARE_lsb           = 32;

parameter EVT_HDR_W2_RUNNUMBER_bits      = 32;
parameter EVT_HDR_W2_RUNNUMBER_msb       = 31;
parameter EVT_HDR_W2_RUNNUMBER_lsb       = 0;

// EVT_HDR_W3 word description
parameter EVT_HDR_W3_bits                = 64;
parameter EVT_HDR_W3_ROI_bits            = 64;
parameter EVT_HDR_W3_ROI_msb             = 63;
parameter EVT_HDR_W3_ROI_lsb             = 0;

// EVT_HDR_W4 word description
parameter EVT_HDR_W4_bits                = 64;
parameter EVT_HDR_W4_EFPU_ID_bits        = 20;
parameter EVT_HDR_W4_EFPU_ID_msb         = 63;
parameter EVT_HDR_W4_EFPU_ID_lsb         = 44;

parameter EVT_HDR_W4_EFPU_PID_bits       = 12;
parameter EVT_HDR_W4_EFPU_PID_msb        = 43;
parameter EVT_HDR_W4_EFPU_PID_lsb        = 32;

parameter EVT_HDR_W4_TIME_bits           = 32;
parameter EVT_HDR_W4_TIME_msb            = 31;
parameter EVT_HDR_W4_TIME_lsb            = 0;

// EVT_HDR_W5 word description
parameter EVT_HDR_W5_bits                = 64;
parameter EVT_HDR_W5_Connection_ID_bits  = 32;
parameter EVT_HDR_W5_Connection_ID_msb   = 63;
parameter EVT_HDR_W5_Connection_ID_lsb   = 32;

parameter EVT_HDR_W5_Transaction_ID_bits = 32;
parameter EVT_HDR_W5_Transaction_ID_msb  = 31;
parameter EVT_HDR_W5_Transaction_ID_lsb  = 0;

// EVT_HDR_W6 word description
parameter EVT_HDR_W6_bits                = 64;
parameter EVT_HDR_W6_STATUS_bits         = 32;
parameter EVT_HDR_W6_STATUS_msb          = 63;
parameter EVT_HDR_W6_STATUS_lsb          = 32;

parameter EVT_HDR_W6_CRC_bits            = 32;
parameter EVT_HDR_W6_CRC_msb             = 31;
parameter EVT_HDR_W6_CRC_lsb             = 0;

parameter EVT_FTR_LWORDS                 = 3;

// EVT_FTR_W1 word description
parameter EVT_FTR_W1_bits                = 64;
parameter EVT_FTR_W1_FLAG_bits           = 8;
parameter EVT_FTR_W1_FLAG_msb            = 63;
parameter EVT_FTR_W1_FLAG_lsb            = 56;
parameter EVT_FTR_W1_FLAG_FLAG           = 205;

parameter EVT_FTR_W1_SPARE_bits          = 8;
parameter EVT_FTR_W1_SPARE_msb           = 55;
parameter EVT_FTR_W1_SPARE_lsb           = 48;

parameter EVT_FTR_W1_META_COUNT_bits     = 16;
parameter EVT_FTR_W1_META_COUNT_msb      = 47;
parameter EVT_FTR_W1_META_COUNT_lsb      = 32;

parameter EVT_FTR_W1_HDR_CRC_bits        = 32;
parameter EVT_FTR_W1_HDR_CRC_msb         = 31;
parameter EVT_FTR_W1_HDR_CRC_lsb         = 0;

// EVT_FTR_W2 word description
parameter EVT_FTR_W2_bits                = 64;
parameter EVT_FTR_W2_ERROR_FLAGS_bits    = 64;
parameter EVT_FTR_W2_ERROR_FLAGS_msb     = 63;
parameter EVT_FTR_W2_ERROR_FLAGS_lsb     = 0;

// EVT_FTR_W3 word description
parameter EVT_FTR_W3_bits                = 64;
parameter EVT_FTR_W3_WORD_COUNT_bits     = 32;
parameter EVT_FTR_W3_WORD_COUNT_msb      = 63;
parameter EVT_FTR_W3_WORD_COUNT_lsb      = 32;

parameter EVT_FTR_W3_CRC_bits            = 32;
parameter EVT_FTR_W3_CRC_msb             = 31;
parameter EVT_FTR_W3_CRC_lsb             = 0;

parameter M_HDR_LWORDS                   = 2;

// M_HDR word description
parameter M_HDR_bits                     = 64;
parameter M_HDR_FLAG_bits                = 8;
parameter M_HDR_FLAG_msb                 = 63;
parameter M_HDR_FLAG_lsb                 = 56;
parameter M_HDR_FLAG_FLAG                = 85;

parameter M_HDR_TYPE_bits                = 2;
parameter M_HDR_TYPE_msb                 = 55;
parameter M_HDR_TYPE_lsb                 = 54;
parameter M_HDR_TYPE_RAW                 = 0;
parameter M_HDR_TYPE_CLUSTERED           = 1;
parameter M_HDR_TYPE_CLUSTEREDwRAW       = 2;
parameter M_HDR_TYPE_UNUSED              = 3;

parameter M_HDR_DET_bits                 = 1;
parameter M_HDR_DET_msb                  = 53;
parameter M_HDR_DET_lsb                  = 53;
parameter M_HDR_DET_PIXEL                = 0;
parameter M_HDR_DET_STRIP                = 1;

parameter M_HDR_ROUTING_bits             = 52;
parameter M_HDR_ROUTING_msb              = 52;
parameter M_HDR_ROUTING_lsb              = 1;
parameter M_HDR_ROUTING_NPRM             = 12;
parameter M_HDR_ROUTING_NAMBUS           = 4;
parameter M_HDR_ROUTING_NTFM_per_SSTP    = 2;
parameter M_HDR_ROUTING_TFM_lsb          = 49; //PRIYA changed , orig 48

parameter M_HDR_SPARE_bits               = 1;
parameter M_HDR_SPARE_msb                = 0;
parameter M_HDR_SPARE_lsb                = 0;

// M_HDR2 word description
parameter M_HDR2_bits                    = 32;
parameter M_HDR2_MODID_bits              = 18;
parameter M_HDR2_MODID_msb               = 31;
parameter M_HDR2_MODID_lsb               = 14;

parameter M_HDR2_MODTYPE_bits            = 2;
parameter M_HDR2_MODTYPE_msb             = 13;
parameter M_HDR2_MODTYPE_lsb             = 12;

parameter M_HDR2_ORIENTATION_bits        = 1;
parameter M_HDR2_ORIENTATION_msb         = 11;
parameter M_HDR2_ORIENTATION_lsb         = 11;

parameter M_HDR2_SPARE_bits              = 11;
parameter M_HDR2_SPARE_msb               = 10;
parameter M_HDR2_SPARE_lsb               = 0;

// HCC_HDR word description
parameter HCC_HDR_bits                   = 16;
parameter HCC_HDR_TYP_bits               = 4;
parameter HCC_HDR_TYP_msb                = 15;
parameter HCC_HDR_TYP_lsb                = 12;
parameter HCC_HDR_TYP_PR                 = 1;
parameter HCC_HDR_TYP_LP                 = 2;

parameter HCC_HDR_FLAG_bits              = 1;
parameter HCC_HDR_FLAG_msb               = 11;
parameter HCC_HDR_FLAG_lsb               = 11;

parameter HCC_HDR_L0ID_bits              = 7;
parameter HCC_HDR_L0ID_msb               = 10;
parameter HCC_HDR_L0ID_lsb               = 4;

parameter HCC_HDR_BCID_bits              = 4;
parameter HCC_HDR_BCID_msb               = 3;
parameter HCC_HDR_BCID_lsb               = 0;

// HCC_CLUSTER word description
parameter HCC_CLUSTER_bits               = 16;
parameter HCC_CLUSTER_UNUSED_bits        = 1;
parameter HCC_CLUSTER_UNUSED_msb         = 15;
parameter HCC_CLUSTER_UNUSED_lsb         = 15;

parameter HCC_CLUSTER_ABC_bits           = 4;
parameter HCC_CLUSTER_ABC_msb            = 14;
parameter HCC_CLUSTER_ABC_lsb            = 11;

parameter HCC_CLUSTER_COL_bits           = 8;
parameter HCC_CLUSTER_COL_msb            = 10;
parameter HCC_CLUSTER_COL_lsb            = 3;

parameter HCC_CLUSTER_NEXT_bits          = 3;
parameter HCC_CLUSTER_NEXT_msb           = 2;
parameter HCC_CLUSTER_NEXT_lsb           = 0;

parameter HCC_LAST_CLUSTER = 16'h6fed;

// PIXEL_CLUSTER word description
parameter PIXEL_CLUSTER_bits             = 32;
parameter PIXEL_CLUSTER_LAST_bits        = 1;
parameter PIXEL_CLUSTER_LAST_msb         = 31;
parameter PIXEL_CLUSTER_LAST_lsb         = 31;

parameter PIXEL_CLUSTER_PHISIZ_bits      = 2;
parameter PIXEL_CLUSTER_PHISIZ_msb       = 30;
parameter PIXEL_CLUSTER_PHISIZ_lsb       = 29;

parameter PIXEL_CLUSTER_PHI_bits         = 13;
parameter PIXEL_CLUSTER_PHI_msb          = 28;
parameter PIXEL_CLUSTER_PHI_lsb          = 16;

parameter PIXEL_CLUSTER_ETASIZ_bits      = 3;
parameter PIXEL_CLUSTER_ETASIZ_msb       = 15;
parameter PIXEL_CLUSTER_ETASIZ_lsb       = 13;

parameter PIXEL_CLUSTER_ETA_bits         = 13;
parameter PIXEL_CLUSTER_ETA_msb          = 12;
parameter PIXEL_CLUSTER_ETA_lsb          = 0;

// PIXEL_CL_FTR word description
parameter PIXEL_CL_FTR_bits              = 32;
parameter PIXEL_CL_FTR_FLAG_bits         = 8;
parameter PIXEL_CL_FTR_FLAG_msb          = 31;
parameter PIXEL_CL_FTR_FLAG_lsb          = 24;
parameter PIXEL_CL_FTR_FLAG_FLAG         = 119;

parameter PIXEL_CL_FTR_COUNT_bits        = 8;
parameter PIXEL_CL_FTR_COUNT_msb         = 23;
parameter PIXEL_CL_FTR_COUNT_lsb         = 16;

parameter PIXEL_CL_FTR_ERROR_bits        = 2;
parameter PIXEL_CL_FTR_ERROR_msb         = 15;
parameter PIXEL_CL_FTR_ERROR_lsb         = 14;
parameter PIXEL_CL_FTR_ERROR_NO_ERROR    = 0;
parameter PIXEL_CL_FTR_ERROR_FRONT_END_ERROR = 1;
parameter PIXEL_CL_FTR_ERROR_PARSE_ERROR = 2;
parameter PIXEL_CL_FTR_ERROR_UNUSED      = 3;

parameter PIXEL_CL_FTR_SPARE_bits        = 14;
parameter PIXEL_CL_FTR_SPARE_msb         = 13;
parameter PIXEL_CL_FTR_SPARE_lsb         = 0;

// STRIP_CLUSTER word description
parameter STRIP_CLUSTER_bits             = 16;
parameter STRIP_CLUSTER_LAST_bits        = 1;
parameter STRIP_CLUSTER_LAST_msb         = 15;
parameter STRIP_CLUSTER_LAST_lsb         = 15;

parameter STRIP_CLUSTER_ROW_bits         = 1;
parameter STRIP_CLUSTER_ROW_msb          = 14;
parameter STRIP_CLUSTER_ROW_lsb          = 14;

parameter STRIP_CLUSTER_LEN_bits         = 3;
parameter STRIP_CLUSTER_LEN_msb          = 13;
parameter STRIP_CLUSTER_LEN_lsb          = 11;

parameter STRIP_CLUSTER_IDX_bits         = 11;
parameter STRIP_CLUSTER_IDX_msb          = 10;
parameter STRIP_CLUSTER_IDX_lsb          = 0;

// STRIP_CL_FTR word description
parameter STRIP_CL_FTR_bits              = 16;
parameter STRIP_CL_FTR_FLAG_bits         = 8;
parameter STRIP_CL_FTR_FLAG_msb          = 15;
parameter STRIP_CL_FTR_FLAG_lsb          = 8;
parameter STRIP_CL_FTR_FLAG_FLAG         = 119;

parameter STRIP_CL_FTR_COUNT_bits        = 6;
parameter STRIP_CL_FTR_COUNT_msb         = 7;
parameter STRIP_CL_FTR_COUNT_lsb         = 2;

parameter STRIP_CL_FTR_ERROR_bits        = 2;
parameter STRIP_CL_FTR_ERROR_msb         = 1;
parameter STRIP_CL_FTR_ERROR_lsb         = 0;
parameter STRIP_CL_FTR_ERROR_NO_ERROR    = 0;
parameter STRIP_CL_FTR_ERROR_FRONT_END_ERROR = 1;
parameter STRIP_CL_FTR_ERROR_PARSE_ERROR = 2;
parameter STRIP_CL_FTR_ERROR_UNUSED      = 3;

parameter TRACK_HDR_LWORDS               = 3;

// TRACK_W1 word description
parameter TRACK_W1_bits                  = 64;
parameter TRACK_W1_TYPE_bits             = 4;
parameter TRACK_W1_TYPE_msb              = 63;
parameter TRACK_W1_TYPE_lsb              = 60;
parameter TRACK_W1_TYPE_FIRST_STAGE      = 1;
parameter TRACK_W1_TYPE_SECOND_STAGE     = 2;

parameter TRACK_W1_PRM_bits              = 10;
parameter TRACK_W1_PRM_msb               = 59;
parameter TRACK_W1_PRM_lsb               = 50;

parameter TRACK_W1_ROADID_bits           = 24;
parameter TRACK_W1_ROADID_msb            = 49;
parameter TRACK_W1_ROADID_lsb            = 26;

parameter TRACK_W1_HITMAP_bits           = 13;
parameter TRACK_W1_HITMAP_msb            = 25;
parameter TRACK_W1_HITMAP_lsb            = 13;

parameter TRACK_W1_DETMAP_bits           = 13;
parameter TRACK_W1_DETMAP_msb            = 12;
parameter TRACK_W1_DETMAP_lsb            = 0;

// TRACK_W2 word description
parameter TRACK_W2_bits                  = 64;
parameter TRACK_W2_STAGE1_SECTOR_bits    = 16;
parameter TRACK_W2_STAGE1_SECTOR_msb     = 63;
parameter TRACK_W2_STAGE1_SECTOR_lsb     = 48;

parameter TRACK_W2_STAGE2_SECTOR_bits    = 16;
parameter TRACK_W2_STAGE2_SECTOR_msb     = 47;
parameter TRACK_W2_STAGE2_SECTOR_lsb     = 32;

parameter TRACK_W2_ETA_bits              = 16;
parameter TRACK_W2_ETA_msb               = 31;
parameter TRACK_W2_ETA_lsb               = 16;

parameter TRACK_W2_PHI_bits              = 16;
parameter TRACK_W2_PHI_msb               = 15;
parameter TRACK_W2_PHI_lsb               = 0;

// TRACK_W3 word description
parameter TRACK_W3_bits                  = 64;
parameter TRACK_W3_QoverPt_bits          = 16;
parameter TRACK_W3_QoverPt_msb           = 63;
parameter TRACK_W3_QoverPt_lsb           = 48;

parameter TRACK_W3_Z0_bits               = 16;
parameter TRACK_W3_Z0_msb                = 47;
parameter TRACK_W3_Z0_lsb                = 32;

parameter TRACK_W3_D0_bits               = 16;
parameter TRACK_W3_D0_msb                = 31;
parameter TRACK_W3_D0_lsb                = 16;

parameter TRACK_W3_CHI2_bits             = 16;
parameter TRACK_W3_CHI2_msb              = 15;
parameter TRACK_W3_CHI2_lsb              = 0;

// TRACK_PIXEL_CLUSTER word description
parameter TRACK_PIXEL_CLUSTER_bits       = 64;
parameter TRACK_PIXEL_CLUSTER_MODID_bits = 18;
parameter TRACK_PIXEL_CLUSTER_MODID_msb  = 63;
parameter TRACK_PIXEL_CLUSTER_MODID_lsb  = 46;

parameter TRACK_PIXEL_CLUSTER_RAW_INCLUDED_bits = 1;
parameter TRACK_PIXEL_CLUSTER_RAW_INCLUDED_msb = 45;
parameter TRACK_PIXEL_CLUSTER_RAW_INCLUDED_lsb = 45;

parameter TRACK_PIXEL_CLUSTER_SPARE_bits = 13;
parameter TRACK_PIXEL_CLUSTER_SPARE_msb  = 44;
parameter TRACK_PIXEL_CLUSTER_SPARE_lsb  = 32;

parameter TRACK_PIXEL_CLUSTER_ETA_bits   = 13;
parameter TRACK_PIXEL_CLUSTER_ETA_msb    = 31;
parameter TRACK_PIXEL_CLUSTER_ETA_lsb    = 19;

parameter TRACK_PIXEL_CLUSTER_PHI_bits   = 13;
parameter TRACK_PIXEL_CLUSTER_PHI_msb    = 18;
parameter TRACK_PIXEL_CLUSTER_PHI_lsb    = 6;

parameter TRACK_PIXEL_CLUSTER_ETASIZ_bits = 3;
parameter TRACK_PIXEL_CLUSTER_ETASIZ_msb = 5;
parameter TRACK_PIXEL_CLUSTER_ETASIZ_lsb = 3;

parameter TRACK_PIXEL_CLUSTER_PHISIZ_bits = 2;
parameter TRACK_PIXEL_CLUSTER_PHISIZ_msb = 2;
parameter TRACK_PIXEL_CLUSTER_PHISIZ_lsb = 1;

parameter TRACK_PIXEL_CLUSTER_LAST_bits  = 1;
parameter TRACK_PIXEL_CLUSTER_LAST_msb   = 0;
parameter TRACK_PIXEL_CLUSTER_LAST_lsb   = 0;

// TRACK_STRIP_CLUSTER word description
parameter TRACK_STRIP_CLUSTER_bits       = 32;
parameter TRACK_STRIP_CLUSTER_MODID_bits = 16;
parameter TRACK_STRIP_CLUSTER_MODID_msb  = 31;
parameter TRACK_STRIP_CLUSTER_MODID_lsb  = 16;

parameter TRACK_STRIP_CLUSTER_ROW_bits   = 1;
parameter TRACK_STRIP_CLUSTER_ROW_msb    = 15;
parameter TRACK_STRIP_CLUSTER_ROW_lsb    = 15;

parameter TRACK_STRIP_CLUSTER_IDX_bits   = 11;
parameter TRACK_STRIP_CLUSTER_IDX_msb    = 14;
parameter TRACK_STRIP_CLUSTER_IDX_lsb    = 4;

parameter TRACK_STRIP_CLUSTER_LEN_bits   = 3;
parameter TRACK_STRIP_CLUSTER_LEN_msb    = 3;
parameter TRACK_STRIP_CLUSTER_LEN_lsb    = 1;

parameter TRACK_STRIP_CLUSTER_LAST_bits  = 1;
parameter TRACK_STRIP_CLUSTER_LAST_msb   = 0;
parameter TRACK_STRIP_CLUSTER_LAST_lsb   = 0;

