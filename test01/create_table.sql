CREATE TABLE `lms.config` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `type` varchar(64) NOT NULL DEFAULT '' COMMENT '类型',
  `code` varchar(64) NOT NULL DEFAULT '' COMMENT '代码',
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '展示名称',
  `parent_code` varchar(64) NOT NULL DEFAULT '' COMMENT '父代码',
  `ext` varchar(255) NOT NULL DEFAULT '' COMMENT '扩充字段',
  `seq` int(11) DEFAULT NULL COMMENT '排序',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态(1:有效;0:无效)',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uniq_type_code` (`type`,`code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=927 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='预定字典配置'
