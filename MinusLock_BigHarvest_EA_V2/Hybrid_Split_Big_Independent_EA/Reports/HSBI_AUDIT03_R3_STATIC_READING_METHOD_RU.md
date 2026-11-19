# AUDIT03 R3 — чтение повторяющихся machine contracts без потери содержания

Это служебный text-view, не evaluator, test runner, новый oracle или evidence об исполнении. Сохраняются порядок полей/элементов, все primitive lexemes, повторные ключи, числа и строки. Удаляется только whitespace вне strings. Точные повторные objects/arrays длиной не менее180 значимых символов заменены локальными @J references; ROOT сохраняет каждое вхождение, определения раскрывают все поля. Полное разворачивание совпало с исходным significant-token stream. Исходные файлы не меняются. FULL назначается только после прочтения ROOT и всех definitions.

## Прочитанный полный view исторического R9-R2 native economic oracle

Source Tests/Contracts/HSB_2E_R4_R9_R2_NATIVE_ECONOMIC_ORACLE.json; SHA256 b2330e1d813cea7d110373116f67ecc8e8e13442aaafcf048c66f9ba0198f9ee; original66150lines/2413675bytes; significant1437410characters; view33172characters. Прочитаны view[0,18000) и[18000,33172), все92definitions. Это не native execution: calculator label говорит INDEPENDENT_STANDARD_LIBRARY_DECIMAL.

~~~text
ROOT={"calculator":"INDEPENDENT_STANDARD_LIBRARY_DECIMAL","expected":[{"expected":@J28,"inputSha256":"df59b683886639f06b4791f5e028543466399179164fbee353224f56f88af13a","vectorId":"R9_INITIAL_001"},{"expected":{"derivationTrace":[@J30,@J31,@J32,@J33,@J34,@J35,@J36,@J37,@J38,@J39,@J40,@J41,@J42,@J43,@J44,@J45,@J46,@J47,{"EXPECTED_VALUE":false,"FORMULA_ID":"SettlementEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"},{"EXPECTED_VALUE":false,"FORMULA_ID":"AllocationEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"},{"EXPECTED_VALUE":false,"FORMULA_ID":"PersistenceEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"},@J48,{"EXPECTED_VALUE":0,"FORMULA_ID":"StateRevisionAfter","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"},{"EXPECTED_VALUE":false,"FORMULA_ID":"CertificateEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}],"reason":"FIXTURE_VALIDATION_REJECTED","status":"REJECT","values":{"AllocatedMoney":"9.0000","AllocationEligibility":false,"AvailableMoney":"12.00","BigActualMoney":"8.00","BigResidualVolume":"0.60","CatchUpRatio":"0.20","CertificateEligibility":false,"CloseFarBudget":"6.0000","FarActualLoss":"20.00","InitialNetActual":"-1.00","NewFarVolume":"0.60","PartialFarVolume":"0.24","PersistenceEligibility":false,"RecoveryPL":"-15.00","RemainingMoney":"3.0000","ReserveAddition":"3.0000","ReserveAfter":"8.0000","ReserveBefore":"5.00","ReserveConsumption":"3.00","ReserveCoverage":true,"SettlementEligibility":false,"SmallActualMoney":"4.00","StateRevisionAfter":0,"StateRevisionBefore":0}},"inputSha256":"2cd7609832791262c36504a94d8a7ac8b689c0cdbacf4d212e08740ed80d3503","vectorId":"R9_INITIAL_002"},{"expected":@J28,"inputSha256":"58f2c88b299b78f25b409738ff377afca94913ad02b9067ce3af842b8fb04aac","vectorId":"R9_INITIAL_003"},{"expected":@J56,"inputSha256":"098102fa1005c6f5b4a23d7ca227e8deac28c0829bdf636033f82942c4af379c","vectorId":"R9_INITIAL_004"},{"expected":@J56,"inputSha256":"29c23add95f18b2e2f1d5b28834463e95d44203c68afbe36bae24b6610b76555","vectorId":"R9_INITIAL_005"},{"expected":@J56,"inputSha256":"81eb7dc5bb7d3a26e47452be3d961513753fafb782bd06135feb6837ee3565ec","vectorId":"R9_INITIAL_006"},{"expected":@J56,"inputSha256":"3d4dffe6afb91638935a548cdfa57e3faa45071db4f3564e9da7ce03862f382d","vectorId":"R9_INITIAL_007"},{"expected":@J28,"inputSha256":"0c72de090d14b8092278b7d83a3cc0409e2d829ab2a2d2557488685043b7a781","vectorId":"R9_INITIAL_008"},{"expected":@J56,"inputSha256":"8c3e5d7f00153dcbbe0285e7cb7452e6433f4cdc5832b7b3cfe5c89f12126e66","vectorId":"R9_INITIAL_009"},{"expected":@J56,"inputSha256":"0c59122be80516ec5c289fdca99308fe6242c7a39d4ebc0fa1c36d4b18eacc7f","vectorId":"R9_INITIAL_010"},{"expected":@J56,"inputSha256":"0d0e66b58ff356b3d6e77445f8d44e24bda1ff4500f1f0553fc49b8243269e98","vectorId":"R9_INITIAL_011"},{"expected":@J28,"inputSha256":"c1674c111c31a2ad00b4628eafc1d5c49303bf9a39560c3eb117dfedd301316b","vectorId":"R9_INITIAL_012"},{"expected":@J28,"inputSha256":"7401cc946e08d51244dbc85a3511966d833ece402b3fd67fb433950373e9a648","vectorId":"R9_BIG_001"},{"expected":@J64,"inputSha256":"dc4be5a9d3383f3ec945da021ab7893286a5eb3f00e1cf5b21dafb59284be828","vectorId":"R9_BIG_002"},{"expected":@J28,"inputSha256":"70079ec231f6bce62db89f4a2fb4823d73d7080c11d4fc1adfa66aea680968df","vectorId":"R9_BIG_003"},{"expected":@J56,"inputSha256":"57d745b014764f3cc5582f6cfd71d296d61c2897072796168913ea3147fe62a9","vectorId":"R9_BIG_004"},{"expected":@J56,"inputSha256":"e090c3d8c6370d980d6fbdb0696a854af0a8857db221c857e1ddfa4795c988c9","vectorId":"R9_BIG_005"},{"expected":@J56,"inputSha256":"f3188787c5a578dcb46b11d6f38c23dce0f20060cfce7c7f80a7f4f0db2fa158","vectorId":"R9_BIG_006"},{"expected":@J56,"inputSha256":"01d555f7dfb61b013254bc6f79683e231412ad28d29a0e7fc203cb99e1ebf519","vectorId":"R9_BIG_007"},{"expected":@J28,"inputSha256":"656915515ab3a0e353d699c74d59cd8c67fa46970e6abf7ce68386ab8b0c8ba7","vectorId":"R9_BIG_008"},{"expected":@J56,"inputSha256":"71f2f0db05418fe27cc00f4a6e50bd596dee6b66ed04886b113f0f438f030c3c","vectorId":"R9_BIG_009"},{"expected":@J56,"inputSha256":"ce3bbb77c7e392869e15b26f0657f2907a35f96714e43800842a907ca128f32c","vectorId":"R9_BIG_010"},{"expected":@J56,"inputSha256":"40f58d5e7dbed36244d3ffd073331fe16aa172cf451fff3f7f87dff9048fbb92","vectorId":"R9_BIG_011"},{"expected":@J28,"inputSha256":"47708d5dc0640ee9f9124b1b97994217f5d7fd4ad244f0a63dfd12926b3abde8","vectorId":"R9_BIG_012"},{"expected":@J56,"inputSha256":"28f250e8c77add7539dcf63b0953b19ad952295f1540aea4487cd7c742471c40","vectorId":"R9_BIG_013"},{"expected":@J56,"inputSha256":"31553b869a09f25f26159d8c005f5d37d5a1741c03b89338394babcee6f883b6","vectorId":"R9_BIG_014"},{"expected":@J92,"inputSha256":"d477c789bb7a239c0ce0243fe4ee63ab45ff709a55fdf987d5551a42278e2024","vectorId":"R9_BIG_015"},{"expected":@J28,"inputSha256":"24a2f532fb32ae3675dc536082f0cca2fa138ded5dda4b2099bf01c2c445e290","vectorId":"R9_BIG_016"},{"expected":@J64,"inputSha256":"98e577b04eaf80312d1646b10b32f498df0af4f67ef46917d5d24039840a01b6","vectorId":"R9_BIG_017"},{"expected":@J28,"inputSha256":"9b502febf03ebcd388ee1a4b4ca1feb64ebb1b768b35640d1602fa4b09dba148","vectorId":"R9_BIG_018"},{"expected":@J56,"inputSha256":"5fb20e21f4f334296bce812a3ccaebc20ec4ac19b236177fcb3a9f1988be9120","vectorId":"R9_BIG_019"},{"expected":@J56,"inputSha256":"24f7308556dd22f1d5e484913bfa06f09005331b03465393bea31c29346a0b05","vectorId":"R9_BIG_020"},{"expected":@J28,"inputSha256":"657047dca7ee9ca448593b9071c12f04955e065915b23180386a9918d2215e08","vectorId":"R9_SMALL_001"},{"expected":@J64,"inputSha256":"5a70524d1c967ad4b944646b7eaff2eceab5536812ff3b312aaf38718ab2d7ea","vectorId":"R9_SMALL_002"},{"expected":@J28,"inputSha256":"8077c4a3e3e1b3d48724f0cfe102903c5b92d45a1648710a8f83f2e2720952dc","vectorId":"R9_SMALL_003"},{"expected":@J56,"inputSha256":"127600ff59401ed572158e3809ee119194f1b6fd15dda8bdcef09db7021e8178","vectorId":"R9_SMALL_004"},{"expected":@J56,"inputSha256":"858b935db9868fc207cd078987fa8c729ea448b7fb1519f5ab1232bd1673e2ab","vectorId":"R9_SMALL_005"},{"expected":@J56,"inputSha256":"c6dcb4b562bc02be924eacdb88414356d5d6a4ab83889f9306cd3dc0e6ffc26c","vectorId":"R9_SMALL_006"},{"expected":@J56,"inputSha256":"15c4b464e5357c9e1c57841a115fc89f5496489cb3dddb475f13323d6fcce949","vectorId":"R9_SMALL_007"},{"expected":@J28,"inputSha256":"01fae6cb9427d244bbd741f4e9822ee6374eed71a0fb6a5924615155ff6303cd","vectorId":"R9_SMALL_008"},{"expected":@J56,"inputSha256":"6ecdd690131ce89fb01484b225c38899729e470dc4205b33f9d80e0951fd5fce","vectorId":"R9_SMALL_009"},{"expected":@J56,"inputSha256":"be0a3b321bc11647f103bd9a5d7698e59958e64187296469f7370cb735c2a2ed","vectorId":"R9_SMALL_010"},{"expected":@J56,"inputSha256":"6b719af8ea486b1f2ecca5759e56364e510766f70269026ee768dd9002760c74","vectorId":"R9_SMALL_011"},{"expected":@J28,"inputSha256":"1e85fd7f71999ca1d0ba0509aab52e92022bea654a880c7daeeb55938c1e194a","vectorId":"R9_SMALL_012"},{"expected":@J56,"inputSha256":"8975aac9e16083bf07001a4cba7f8df87762cfb8a8a7204492bfaf82f2120f26","vectorId":"R9_SMALL_013"},{"expected":@J56,"inputSha256":"d3aa5a856183a26b7b3faa16a5115931406fa401745d866b48a32a337dcf9c85","vectorId":"R9_SMALL_014"},{"expected":@J92,"inputSha256":"22b9ccb7f360fb8a6cb957a5f85dbfca98a24608a129c25c1293b510c0e0d65c","vectorId":"R9_SMALL_015"},{"expected":@J28,"inputSha256":"0c73e0031a8f4587065944631db826270c975cf7c17b82ca77939ca757ff7688","vectorId":"R9_SMALL_016"},{"expected":@J64,"inputSha256":"1a0d7cac33edb0b9dbd36d0a88a92ad945f04d7fa678b2e0f04c1bbd7f0e702b","vectorId":"R9_SMALL_017"},{"expected":@J28,"inputSha256":"0d7b898b97355e7333b9f1ed28539a4e13e50f458c0f511a9467dfac50436fe4","vectorId":"R9_SMALL_018"},{"expected":@J56,"inputSha256":"382cb57f893a490cbe46b31644a73a7b0f51c28513557186b50f1b328f5348aa","vectorId":"R9_SMALL_019"},{"expected":@J56,"inputSha256":"5da4879f5bf19adbff8381c9a957cff656d2aa6d1d7f0408e03f57ac1dd6c1b4","vectorId":"R9_SMALL_020"},{"expected":@J28,"inputSha256":"49418b052d06129ec5c3b970307c7771bfa944df6cb0c14f27f2a002d2dab805","vectorId":"R9_FINAL_001"},{"expected":@J64,"inputSha256":"7300c1397b718605c9e2e642d4296c5fd40f7633ac0c76542ae1c6dce3f98c37","vectorId":"R9_FINAL_002"},{"expected":@J28,"inputSha256":"6dc590767267cb2a52dee7e3b1a75592a314c5bbead2cb8a079199af85e40418","vectorId":"R9_FINAL_003"},{"expected":@J56,"inputSha256":"ce2c1cd27ad877a854fcddb1812674ce86a0e473d2039910e733977093efc001","vectorId":"R9_FINAL_004"},{"expected":@J56,"inputSha256":"6df5ededc64d80f5c0015157e69fcf31bf4236a32253774bf78fd5c4b9389249","vectorId":"R9_FINAL_005"},{"expected":@J56,"inputSha256":"96e112871399eeb6a56d2c14355f6ed1d65f3d7decea7a5cbec852129647d582","vectorId":"R9_FINAL_006"},{"expected":@J56,"inputSha256":"a1c6de7d305b3eda09cbc2fe2b530625921cfbe82738ee3cb77ec0f3cc5dd379","vectorId":"R9_FINAL_007"},{"expected":@J28,"inputSha256":"9ef9ae7f1c77921832299a27833a50cb826f84c99f8e563a51dbad398349ba98","vectorId":"R9_FINAL_008"},{"expected":@J56,"inputSha256":"010ad62cf2aaf012d5fe80248ad61c030630190c15b51d30c4705f1c987d84c1","vectorId":"R9_FINAL_009"},{"expected":@J56,"inputSha256":"85560d6c0326adf041a1432b9770b109434992cfbc10b1b0eed2de416b57cc71","vectorId":"R9_FINAL_010"},{"expected":@J56,"inputSha256":"5d9e0892d035918edecf4a02080238f0b6935f4bf075bb828d90e48e13128a6a","vectorId":"R9_FINAL_011"},{"expected":@J28,"inputSha256":"3056b035f5cf417e6aecdd78f018c3766c7ed58bf095fd75a19b89843ac3bd76","vectorId":"R9_FINAL_012"},{"expected":@J56,"inputSha256":"00573ab4c62fdd478031648361f517ac4a1b07bf66e5f718cb9e2146f9525963","vectorId":"R9_FINAL_013"},{"expected":@J56,"inputSha256":"c9bdbe5faf3687533cd883a70e8f9e18a9efbe796f7507dc4958b05dcad9c1bf","vectorId":"R9_FINAL_014"},{"expected":@J92,"inputSha256":"0788a73237d134b38c2bf0b317231b26eb9c91c5a61d1dc70061205158a87fea","vectorId":"R9_FINAL_015"},{"expected":@J28,"inputSha256":"4cfd5a8f5b33b6a482255f1b80e9f4e42c75f9b783b583cf762d32d685ffc87f","vectorId":"R9_FINAL_016"},{"expected":@J28,"inputSha256":"bf35134dad5301c6da7fcfa62e5ad3b547e60150919d5cfeb9b8e0353882dd6e","vectorId":"R9_RESTART_CONTINUATION_001"},{"expected":@J64,"inputSha256":"3f8b8bd7313891c48034046f807c44104e93a4dad426f6787343f20ccf5af9dd","vectorId":"R9_RESTART_CONTINUATION_002"},{"expected":@J28,"inputSha256":"9d0a93738cee65b732ea9ec2f6dea563df18e055fa25d04965daf75195cf422b","vectorId":"R9_RESTART_CONTINUATION_003"},{"expected":@J56,"inputSha256":"4496bf992cd6a0b403dfa255a9541dd1645d29a85afd553f47f2eddd528760eb","vectorId":"R9_RESTART_CONTINUATION_004"},{"expected":@J56,"inputSha256":"9cc56ae1da2869c5a4329e2b468dce54742b79fced1993e9b18d3cefb422911f","vectorId":"R9_RESTART_CONTINUATION_005"},{"expected":@J56,"inputSha256":"2532fcdcb45cf2749bbf1a41e297a86d21ad430dd84edf38456ce7fa29671962","vectorId":"R9_RESTART_CONTINUATION_006"},{"expected":@J56,"inputSha256":"d6ca1285210f74c304438cd3765975335465346013615dd9723c35c275b9e22d","vectorId":"R9_RESTART_CONTINUATION_007"},{"expected":@J28,"inputSha256":"50d7c4f718d5cd3f2847652982cffb60e9232ff56ee70ba029b10a297eb0d7be","vectorId":"R9_RESTART_CONTINUATION_008"},{"expected":@J56,"inputSha256":"653f1af0b0554a6d7dfd9b7d9d41ae9f018f9531aab644a3e3b5194759d0958f","vectorId":"R9_RESTART_CONTINUATION_009"},{"expected":@J56,"inputSha256":"9d80ff442e574be12617ccc0e2356ca1f5aab0b58e3e0baa0ed00ec22163aa80","vectorId":"R9_RESTART_CONTINUATION_010"},{"expected":@J56,"inputSha256":"3eadb30a57cf8e5d1f033bcf2f91c81d444704d717c8036e55a799547a900a51","vectorId":"R9_RESTART_CONTINUATION_011"},{"expected":@J28,"inputSha256":"ff808325f807a6395ad0a1cb09edd6ed09feca927380625d2272289d364557c0","vectorId":"R9_RESTART_CONTINUATION_012"},{"expected":@J28,"inputSha256":"b094e9557d7e89680a9a1a0bb0495d45dbb15b252fa01db7e9168dec93813bdd","vectorId":"R9_REPLAY_COMMITTED_001"},{"expected":@J64,"inputSha256":"aa447bed1f6655cbf6354d3a5ecdda2dde165f10232c45d0859177c5b34d973a","vectorId":"R9_REPLAY_COMMITTED_002"},{"expected":@J28,"inputSha256":"0d88a7caecf544c6b9ace72223ecaec09eeed7d914090cf7e5d9be648a8225be","vectorId":"R9_REPLAY_COMMITTED_003"},{"expected":@J56,"inputSha256":"9ac543536633b65a7a123c0824f255227e1276516d3372db09dd871b6f767235","vectorId":"R9_REPLAY_COMMITTED_004"},{"expected":@J56,"inputSha256":"558cbabbcf6414c0358361b5e1056fe3e1b7134d07d858a63c24fcebdfbf75c5","vectorId":"R9_REPLAY_COMMITTED_005"},{"expected":@J56,"inputSha256":"b29d264defbf2cf872bf29b60c74c64df2b170f4716e28cc1a88b2b4915b7971","vectorId":"R9_REPLAY_COMMITTED_006"},{"expected":@J56,"inputSha256":"b9bd3d5e7e79aa03d98e8a83ae2954f2768d246ff2f8d7ebb5b8875431237589","vectorId":"R9_REPLAY_COMMITTED_007"},{"expected":@J28,"inputSha256":"5dbf23f3f28acce36f49107bd5ff82d52a2924e7d7e9f25fc83c0c0ba89bafe6","vectorId":"R9_REPLAY_COMMITTED_008"},{"expected":@J56,"inputSha256":"e18ccf410ef0af0a289072522a968e76553a16e2df66b82623d623a501cdd96e","vectorId":"R9_REPLAY_COMMITTED_009"},{"expected":@J56,"inputSha256":"55353be7454d0c34db00c799849d041d47e81a085a24f5a190122ee7427db9ba","vectorId":"R9_REPLAY_COMMITTED_010"},{"expected":@J56,"inputSha256":"7b90d87d1c20ce4d28de7f97d8c34201b7c49546d1ad5d1d848eea3b9ee5dd59","vectorId":"R9_REPLAY_COMMITTED_011"},{"expected":@J28,"inputSha256":"0e688d4d4b4a2d31647835a5d4b0f4eef4e18aa643965d20ab509581d790d275","vectorId":"R9_REPLAY_COMMITTED_012"},{"expected":@J28,"inputSha256":"6186ae70a41d4faaa0927087a6586fea490cb182f0dfeddba454b036634a8198","vectorId":"R9_LIFECYCLE_001"},{"expected":@J64,"inputSha256":"46bcc0e5d8d67040bd1bad0fd9b1564f039c84cfe80b21723ae01208f180e1c6","vectorId":"R9_LIFECYCLE_002"},{"expected":@J28,"inputSha256":"afc71a86a6487c381f6388604b5c0d551756144b0254ef22ab0a4570889fb708","vectorId":"R9_LIFECYCLE_003"},{"expected":@J56,"inputSha256":"6663668933377d39a791ca2dd028d3281cba2ee3ea845e97dbd5737e4b8d75e8","vectorId":"R9_LIFECYCLE_004"},{"expected":@J56,"inputSha256":"64a4b3525a2d5470ac8bb6a5687273fdce20769e0adb033d29cd44b0a9c50149","vectorId":"R9_LIFECYCLE_005"},{"expected":@J56,"inputSha256":"5af92d23faa11f7b530eecc4dfd283885c7f49fb7e5e599e9f13fc0afd1d2ddd","vectorId":"R9_LIFECYCLE_006"},{"expected":@J56,"inputSha256":"957edfbc0b415b469a5cb879043a6d15a3bca47b1473c78991f4a82ceea63d40","vectorId":"R9_LIFECYCLE_007"},{"expected":@J28,"inputSha256":"58a08ae8d3c5595f37b05cb422b051945db452591cccbf8a572ae2c48a7d1bfc","vectorId":"R9_LIFECYCLE_008"},{"expected":@J56,"inputSha256":"d705ff0028aa1d0058d3f1d101bff15f616cff3803ebf2bd989c7b8c0a4bad58","vectorId":"R9_LIFECYCLE_009"},{"expected":@J56,"inputSha256":"9560bcbb0e64c30c660c603df18e44d063b13d5e7e39171807485a2c50b3814d","vectorId":"R9_LIFECYCLE_010"},{"expected":@J56,"inputSha256":"63347f533b36f59af88323c3039c3ef749cfcc7e3d02254c049632c4e97962a3","vectorId":"R9_LIFECYCLE_011"},{"expected":@J28,"inputSha256":"d9d311e12f548c7e97841b86f4d27ecb3b290e667e4c2455b3fd716023ed854c","vectorId":"R9_LIFECYCLE_012"}],"schemaVersion":1}
@J1={"bigClosedConfirmed":"0.40","bigNet":"8.00","bigVolumeBefore":"1.00","closeFarShare":"0.50","controlDistance":"0.01000","farActualLoss":"20.00","farVolume":"0.80","initialNet":"10.00","lossPerLot":"25.00","movementToBig":"0.00500","recoveryPLBefore":"5.00","requiredCoverage":"3.00","reserveBefore":"5.00","reserveShare":"0.25","smallNet":"4.00","smallReserveShare":"0.25"}
@J2={"EXPECTED_VALUE":"10.00","FORMULA_ID":"InitialNetActual","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J3={"EXPECTED_VALUE":"8.00","FORMULA_ID":"BigActualMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J4={"EXPECTED_VALUE":"4.00","FORMULA_ID":"SmallActualMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J5={"EXPECTED_VALUE":"20.00","FORMULA_ID":"FarActualLoss","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J6={"EXPECTED_VALUE":"12.00","FORMULA_ID":"AvailableMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J7={"EXPECTED_VALUE":"6.0000","FORMULA_ID":"CloseFarBudget","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J8={"EXPECTED_VALUE":"3.0000","FORMULA_ID":"ReserveAddition","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J9={"EXPECTED_VALUE":"5.00","FORMULA_ID":"ReserveBefore","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J10={"EXPECTED_VALUE":"8.0000","FORMULA_ID":"ReserveAfter","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J11={"EXPECTED_VALUE":"0.24","FORMULA_ID":"PartialFarVolume","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J12={"EXPECTED_VALUE":"0.60","FORMULA_ID":"BigResidualVolume","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J13={"EXPECTED_VALUE":"0.60","FORMULA_ID":"NewFarVolume","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J14={"EXPECTED_VALUE":"0.20","FORMULA_ID":"CatchUpRatio","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J15={"EXPECTED_VALUE":"-15.00","FORMULA_ID":"RecoveryPL","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J16={"EXPECTED_VALUE":true,"FORMULA_ID":"ReserveCoverage","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J17={"EXPECTED_VALUE":"3.00","FORMULA_ID":"ReserveConsumption","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J18={"EXPECTED_VALUE":"9.0000","FORMULA_ID":"AllocatedMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J19={"EXPECTED_VALUE":"3.0000","FORMULA_ID":"RemainingMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J20={"EXPECTED_VALUE":true,"FORMULA_ID":"SettlementEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J21={"EXPECTED_VALUE":true,"FORMULA_ID":"AllocationEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J22={"EXPECTED_VALUE":true,"FORMULA_ID":"PersistenceEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J23={"EXPECTED_VALUE":0,"FORMULA_ID":"StateRevisionBefore","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J24={"EXPECTED_VALUE":1,"FORMULA_ID":"StateRevisionAfter","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J25={"EXPECTED_VALUE":true,"FORMULA_ID":"CertificateEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J26=[@J2,@J3,@J4,@J5,@J6,@J7,@J8,@J9,@J10,@J11,@J12,@J13,@J14,@J15,@J16,@J17,@J18,@J19,@J20,@J21,@J22,@J23,@J24,@J25]
@J27={"AllocatedMoney":"9.0000","AllocationEligibility":true,"AvailableMoney":"12.00","BigActualMoney":"8.00","BigResidualVolume":"0.60","CatchUpRatio":"0.20","CertificateEligibility":true,"CloseFarBudget":"6.0000","FarActualLoss":"20.00","InitialNetActual":"10.00","NewFarVolume":"0.60","PartialFarVolume":"0.24","PersistenceEligibility":true,"RecoveryPL":"-15.00","RemainingMoney":"3.0000","ReserveAddition":"3.0000","ReserveAfter":"8.0000","ReserveBefore":"5.00","ReserveConsumption":"3.00","ReserveCoverage":true,"SettlementEligibility":true,"SmallActualMoney":"4.00","StateRevisionAfter":1,"StateRevisionBefore":0}
@J28={"derivationTrace":@J26,"reason":"COMMITTED","status":"PASS","values":@J27}
@J29={"bigClosedConfirmed":"0.40","bigNet":"8.00","bigVolumeBefore":"1.00","closeFarShare":"0.50","controlDistance":"0.01000","farActualLoss":"20.00","farVolume":"0.80","initialNet":"-1.00","lossPerLot":"25.00","movementToBig":"0.00500","recoveryPLBefore":"5.00","requiredCoverage":"3.00","reserveBefore":"5.00","reserveShare":"0.25","smallNet":"4.00","smallReserveShare":"0.25"}
@J30={"EXPECTED_VALUE":"-1.00","FORMULA_ID":"InitialNetActual","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J31={"EXPECTED_VALUE":"8.00","FORMULA_ID":"BigActualMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J32={"EXPECTED_VALUE":"4.00","FORMULA_ID":"SmallActualMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J33={"EXPECTED_VALUE":"20.00","FORMULA_ID":"FarActualLoss","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J34={"EXPECTED_VALUE":"12.00","FORMULA_ID":"AvailableMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J35={"EXPECTED_VALUE":"6.0000","FORMULA_ID":"CloseFarBudget","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J36={"EXPECTED_VALUE":"3.0000","FORMULA_ID":"ReserveAddition","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J37={"EXPECTED_VALUE":"5.00","FORMULA_ID":"ReserveBefore","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J38={"EXPECTED_VALUE":"8.0000","FORMULA_ID":"ReserveAfter","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J39={"EXPECTED_VALUE":"0.24","FORMULA_ID":"PartialFarVolume","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J40={"EXPECTED_VALUE":"0.60","FORMULA_ID":"BigResidualVolume","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J41={"EXPECTED_VALUE":"0.60","FORMULA_ID":"NewFarVolume","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J42={"EXPECTED_VALUE":"0.20","FORMULA_ID":"CatchUpRatio","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J43={"EXPECTED_VALUE":"-15.00","FORMULA_ID":"RecoveryPL","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J44={"EXPECTED_VALUE":true,"FORMULA_ID":"ReserveCoverage","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J45={"EXPECTED_VALUE":"3.00","FORMULA_ID":"ReserveConsumption","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J46={"EXPECTED_VALUE":"9.0000","FORMULA_ID":"AllocatedMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J47={"EXPECTED_VALUE":"3.0000","FORMULA_ID":"RemainingMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J48={"EXPECTED_VALUE":0,"FORMULA_ID":"StateRevisionBefore","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J49={"EXPECTED_VALUE":false,"FORMULA_ID":"SettlementEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J50={"EXPECTED_VALUE":false,"FORMULA_ID":"AllocationEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J51={"EXPECTED_VALUE":false,"FORMULA_ID":"PersistenceEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J52={"EXPECTED_VALUE":0,"FORMULA_ID":"StateRevisionAfter","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J53={"EXPECTED_VALUE":false,"FORMULA_ID":"CertificateEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J1,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J54=[@J2,@J3,@J4,@J5,@J6,@J7,@J8,@J9,@J10,@J11,@J12,@J13,@J14,@J15,@J16,@J17,@J18,@J19,@J49,@J50,@J51,@J23,@J52,@J53]
@J55={"AllocatedMoney":"9.0000","AllocationEligibility":false,"AvailableMoney":"12.00","BigActualMoney":"8.00","BigResidualVolume":"0.60","CatchUpRatio":"0.20","CertificateEligibility":false,"CloseFarBudget":"6.0000","FarActualLoss":"20.00","InitialNetActual":"10.00","NewFarVolume":"0.60","PartialFarVolume":"0.24","PersistenceEligibility":false,"RecoveryPL":"-15.00","RemainingMoney":"3.0000","ReserveAddition":"3.0000","ReserveAfter":"8.0000","ReserveBefore":"5.00","ReserveConsumption":"3.00","ReserveCoverage":true,"SettlementEligibility":false,"SmallActualMoney":"4.00","StateRevisionAfter":0,"StateRevisionBefore":0}
@J56={"derivationTrace":@J54,"reason":"FIXTURE_VALIDATION_REJECTED","status":"REJECT","values":@J55}
@J57={"EXPECTED_VALUE":true,"FORMULA_ID":"SettlementEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J58={"EXPECTED_VALUE":true,"FORMULA_ID":"AllocationEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J59={"EXPECTED_VALUE":true,"FORMULA_ID":"PersistenceEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J60={"EXPECTED_VALUE":1,"FORMULA_ID":"StateRevisionAfter","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J61={"EXPECTED_VALUE":true,"FORMULA_ID":"CertificateEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J29,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J62=[@J30,@J31,@J32,@J33,@J34,@J35,@J36,@J37,@J38,@J39,@J40,@J41,@J42,@J43,@J44,@J45,@J46,@J47,@J57,@J58,@J59,@J48,@J60,@J61]
@J63={"AllocatedMoney":"9.0000","AllocationEligibility":true,"AvailableMoney":"12.00","BigActualMoney":"8.00","BigResidualVolume":"0.60","CatchUpRatio":"0.20","CertificateEligibility":true,"CloseFarBudget":"6.0000","FarActualLoss":"20.00","InitialNetActual":"-1.00","NewFarVolume":"0.60","PartialFarVolume":"0.24","PersistenceEligibility":true,"RecoveryPL":"-15.00","RemainingMoney":"3.0000","ReserveAddition":"3.0000","ReserveAfter":"8.0000","ReserveBefore":"5.00","ReserveConsumption":"3.00","ReserveCoverage":true,"SettlementEligibility":true,"SmallActualMoney":"4.00","StateRevisionAfter":1,"StateRevisionBefore":0}
@J64={"derivationTrace":@J62,"reason":"COMMITTED","status":"PASS","values":@J63}
@J65={"bigClosedConfirmed":"0.40","bigNet":"8.00","bigVolumeBefore":"1.00","closeFarShare":"0.75","controlDistance":"0.01000","farActualLoss":"20.00","farVolume":"0.80","initialNet":"10.00","lossPerLot":"25.00","movementToBig":"0.00500","recoveryPLBefore":"5.00","requiredCoverage":"3.00","reserveBefore":"5.00","reserveShare":"0.75","smallNet":"4.00","smallReserveShare":"0.25"}
@J66={"EXPECTED_VALUE":"10.00","FORMULA_ID":"InitialNetActual","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J67={"EXPECTED_VALUE":"8.00","FORMULA_ID":"BigActualMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J68={"EXPECTED_VALUE":"4.00","FORMULA_ID":"SmallActualMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J69={"EXPECTED_VALUE":"20.00","FORMULA_ID":"FarActualLoss","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J70={"EXPECTED_VALUE":"12.00","FORMULA_ID":"AvailableMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J71={"EXPECTED_VALUE":"9.0000","FORMULA_ID":"CloseFarBudget","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J72={"EXPECTED_VALUE":"9.0000","FORMULA_ID":"ReserveAddition","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J73={"EXPECTED_VALUE":"5.00","FORMULA_ID":"ReserveBefore","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J74={"EXPECTED_VALUE":"14.0000","FORMULA_ID":"ReserveAfter","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J75={"EXPECTED_VALUE":"0.36","FORMULA_ID":"PartialFarVolume","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J76={"EXPECTED_VALUE":"0.60","FORMULA_ID":"BigResidualVolume","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J77={"EXPECTED_VALUE":"0.60","FORMULA_ID":"NewFarVolume","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J78={"EXPECTED_VALUE":"0.35","FORMULA_ID":"CatchUpRatio","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J79={"EXPECTED_VALUE":"-15.00","FORMULA_ID":"RecoveryPL","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J80={"EXPECTED_VALUE":true,"FORMULA_ID":"ReserveCoverage","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J81={"EXPECTED_VALUE":"3.00","FORMULA_ID":"ReserveConsumption","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J82={"EXPECTED_VALUE":"18.0000","FORMULA_ID":"AllocatedMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J83={"EXPECTED_VALUE":"-6.0000","FORMULA_ID":"RemainingMoney","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J84={"EXPECTED_VALUE":false,"FORMULA_ID":"SettlementEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J85={"EXPECTED_VALUE":false,"FORMULA_ID":"AllocationEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J86={"EXPECTED_VALUE":false,"FORMULA_ID":"PersistenceEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J87={"EXPECTED_VALUE":0,"FORMULA_ID":"StateRevisionBefore","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J88={"EXPECTED_VALUE":0,"FORMULA_ID":"StateRevisionAfter","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J89={"EXPECTED_VALUE":false,"FORMULA_ID":"CertificateEligibility","INPUT_UNITS":"ACCOUNT_MONEY_OR_LOTS","INPUT_VALUES":@J65,"INTERMEDIATE_VALUES":{},"ROUNDING_POLICY":"ROUND_DOWN"}
@J90=[@J66,@J67,@J68,@J69,@J70,@J71,@J72,@J73,@J74,@J75,@J76,@J77,@J78,@J79,@J80,@J81,@J82,@J83,@J84,@J85,@J86,@J87,@J88,@J89]
@J91={"AllocatedMoney":"18.0000","AllocationEligibility":false,"AvailableMoney":"12.00","BigActualMoney":"8.00","BigResidualVolume":"0.60","CatchUpRatio":"0.35","CertificateEligibility":false,"CloseFarBudget":"9.0000","FarActualLoss":"20.00","InitialNetActual":"10.00","NewFarVolume":"0.60","PartialFarVolume":"0.36","PersistenceEligibility":false,"RecoveryPL":"-15.00","RemainingMoney":"-6.0000","ReserveAddition":"9.0000","ReserveAfter":"14.0000","ReserveBefore":"5.00","ReserveConsumption":"3.00","ReserveCoverage":true,"SettlementEligibility":false,"SmallActualMoney":"4.00","StateRevisionAfter":0,"StateRevisionBefore":0}
@J92={"derivationTrace":@J90,"reason":"FIXTURE_VALIDATION_REJECTED","status":"REJECT","values":@J91}
~~~

## Границы вывода

104 vectorId/inputhash bindings сохранены; repeated financial expected profiles не104 независимых экономических proofs. Trace INPUT_UNITS=ACCOUNT_MONEY_OR_LOTS неоднозначен по размерностям, INTERMEDIATE_VALUES пустые. PASS/COMMITTED и REJECT сохраняют рассчитанные numeric fields, но rejected numbers не деньги/commit. Overshare profile имеет Remaining−6 и SettlementEligibility=false — это отвергнутый пример, не доказанное создание денег. InitialNet и Small-source attribution относятся историческому profile, не новым утверждённым решениям. inputSHA должен отдельно связываться с fixtures; exacttextreading не подтверждает independence/корректность всехexpected. Historical V1 superseded из-за certificate-forgery metadata-only; ERR013/022/027/028/029/033/047, F007/F013/F019/F035/F042/F053/F057/F060/F062, IMP001/004/009/014/017/018.


## Requirement matrix: точное переиспользование ранее прочитанных строк

R3: полностью прочитано source-linked представление всех исходных токенов: ROOT +240 достижимых definitions +4 key templates;1288 точных Text-ссылок на34 ранее FULL и неизменных источника. Полный view95178символов прочитан диапазонами0–18000–36000–54000–72000–90000–95178; метод/representation сохранены отдельно. ManualSections15,Rows1288,CodeToRequirement199,ModuleReview74: групповые verdict не являются индивидуальным clause proof. Нативные результаты NOT_RUN; no financial execution. ERR013/016/027/028/033/047; F036/053/057/060/062.

@ROWS перечисляет все line ranges и последовательные ordinal; ID=prefix+"-L"+line+"-"+ordinal. Всякое новое поле и отличие сохраняется. @SOURCE_LINE допустим только при точном совпадении JSON-лексемы с указанной строкой полностью прочитанного источника; источник не заменяется заголовком или поиском. Неиспользуемые @J definitions исключены из view, поскольку их полные значения уже раскрыты в source links. Это статическое текстовое представление, а не тест модели.

Исходный SHA256: 81df84e0fb5f66ae3f944cd8d696e42ca2d8cc72f311904456cea1172b18af4b

### Source hashes

- Docs/00_PROJECT_CHARTER_RU.md: c9ff704552eb28a4e8694ca848adf8f8b230280b0ec6fae488e194654a4bbbee
- Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md: ef241eaa1afc6552e420d9bb486740e8cfb160b7f94f349beb0da25725c2d1b4
- Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md: 9da85416f62b292676489080e2d7a92166183d4d7dc027aaee875bffd644e145
- Docs/03_FULL_SYSTEM_MANUAL_RU.md: 3d0bd17b2501d61d612d6ec982b215d52dbd92da8b174d4e425f4c477c7484d0
- Docs/04_MATHEMATICAL_MODEL_RU.md: 1c0ff82d1cbec0179779604b9b7fc9f52f70e74daa25ad2013178984a0758ac2
- Docs/05_GEOMETRY_MODEL_RU.md: e360b8bdf7b456200f1d9b8ef9eafdfe8c30299ff4a3a74383a40e2eb441982d
- Docs/06_STATE_MACHINE_SPECIFICATION_RU.md: b8d5fa9b36d85f5ed59cfaedfb5f748ca3615a163fdb544758367f0510201d77
- Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md: 5e9f4669bdbaff85521e14c1b5d097a81e3f752b8edd61b0ca2618bb5356cc72
- Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md: c49debcc4d65d9a1949b82e8a8aa857c8a465a01a80aea55caddc21e71231133
- Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md: 6c84edbe7dc7b8ab0b652ab9ce484312e6ec031e3d2e82ebbea6ee5bc19f8f5b
- Docs/10_BIG_HARVEST_SPECIFICATION_RU.md: 5dd201cb5b8fbb70410af2976b011ed7e000736edb24bcd565409f6259d47a4d
- Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md: 3ed00ad5988f8de2bbd0ed8e93dd0825b7d7085f61898c594d8001d6cc6f5550
- Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md: a4448a415ad3cd9d5e6cbcd97d5f19a8ae9dfa025087841d03662bb3532ee4f3
- Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md: a1b1ad4d223affc93a6316fe9a955804be19a5a2d050d5dffdb828cda2c7c4f0
- Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md: cd8e312bc8d98519f42618b2ac3f316be546f178f4cc0b3168577bb365603dc1
- Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md: f3a9b58051324e7b07e6a9d33b57cd6691a5c3dbfbafd827b136689b349f093b
- Docs/16_PERSISTENCE_AND_RESTART_RU.md: a406e4caed5b8bf2be156a9a72c461caf51744562fdd6db4f92782263968e588
- Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md: 7539f7fc414fb8ea855939ed91ae5507f80ef3603357275834fc487eda4d2757
- Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md: ffa4dc5fec0679144285f7e8b9ebc8119b65b2c2e62136868a4d84bb213f43e9
- Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md: 068792e3ff986ca8f02545eb8eb6901fe392fd6a2c57cae6040d604144011af2
- Docs/20_TEST_STRATEGY_RU.md: 0c924c5048bdb4ab9592160ff5161f3f109470befffee2961385faee51ff592b
- Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md: a0e32d8424b31a159da6664fbe88db5823c8ef93110b9a82c07685512a69aca4
- Docs/22_OPEN_DECISIONS_REGISTER_RU.md: d838fee32a42366505afdb0856d3c40a5ff6abff01efdf1942ed59452e20f2b6
- Docs/23_NORMATIVE_DECISIONS_RESOLUTION_RU.md: 278a7cf7aefb49154e607d7403094b9f14466b9db743c7379a988142543860c6
- Docs/24_BROKER_MONEY_MODEL_RU.md: d94371024898ab9e00e89f2d4505fc5ccdac7be229e55630676ad0ea6ad51b7c
- Docs/25_BROKER_GRID_AND_ROUNDING_RU.md: f961f9fe4b285776f53c61260422b6edd0aba4781b8e67d5e44ae362d5248476
- Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md: cd4e22f4b69e33dd03e1b079e7058b35180c6f6b624cafb1e7a7f4a27fa4224c
- Docs/27_CONTROL_PRICES_AND_COSTS_RU.md: 6d4e247509f518fa80e628d0adc28782e579252db6dec0d7bdefcad35edcd2d2
- Docs/27_FUTURE_SMALL_SOLVER_RU.md: 0fb2e7c2696b5d12039234a7598a0b389785da1daeabf65dcefaa56885db1798
- Docs/28_NEW_FAR_SOLVER_RU.md: 44d5fbb9d285ab40ccf1b98f481d3ceb5ce5406466e67e78be581f96b9cd0205
- Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md: a78120ffb2d6d9646ce721252237633e7aef1f775da5e472f0e66a7b92158bf8
- Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md: c5eed7cb353842f38ca8de6c117bb6e8fb165503ab59c15ec201b6063f2514c4
- Docs/31_MONEY_PROOF_IDENTITY_RU.md: a9bdc39ea52ab5dc19db21d94055e50a10c30d85da04925aad5eab440d831330
- Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md: 7112c87534718292e102e71d6ff33602dbfdff522022e3b92a32aae0dff043d5

### Полное представление

```text
ROOT={"BaseSHA":@J1,"TestedSHA":@J1,"UTC":"2026-11-11T20:16:08.675810+00:00","RunnerSourceHash":"9e5144c1096a966272e08bb2be1a2f0865f6e45421d470982420e70d99f88515","ApprovalStatus":"AWAITING_ADMIN_APPROVAL","ManualSections":[@T1("Полный цикл",@J2,5,7,@J3,"UNIMPLEMENTED",@J4,@J5,@J6),@T1("Роли и направления",@J2,8,10,@J7,"PARTIALLY_VERIFIED",@J4,@J5,@J6),@T1("Объёмы и три закона",@J2,11,13,@J8,"CONTRADICTORY",@J4,@J5,@J6),@T1("Typed control prices",@J2,14,16,@J9,"PARTIALLY_VERIFIED",@J4,@J5,@J6),@T1(@J10,@J2,17,19,@J11,"CONTRADICTORY",@J4,@J5,@J6),@T1("NewFar",@J2,20,22,@J12,"CONTRADICTORY",@J4,@J5,@J6),@T1("Money и allocation",@J2,23,25,@J13,"CONTRADICTORY",@J4,@J5,@J6),@T1("Partial Far",@J2,26,28,@J14,"UNIMPLEMENTED",@J4,@J5,@J6),@T1("Transition Loss",@J2,29,31,@J15,"PARTIALLY_VERIFIED",@J4,@J5,@J6),@T1("Final Close",@J2,32,34,@J16,"UNIMPLEMENTED",@J4,@J5,@J6),@T1("Small confirmation",@J2,35,37,@J17,"UNIMPLEMENTED",@J4,@J5,@J6),@T1(@J18,@J2,38,40,@J19,"UNIMPLEMENTED",@J4,@J5,@J6),@T1("Risk, margin и emergency",@J2,41,43,@J20,"CONTRADICTORY",@J4,@J5,@J6),@T1(@J21,@J2,44,46,@J22,"UNIMPLEMENTED",@J4,@J5,@J6),@T1("Restart/error semantics",@J2,47,51,"Restart сверяет actual positions/orders/deals, snapshot и action/event ledgers. Нельзя угадывать FAR, восстанавливать только по comment или продолжать после conflict. Critical mismatch → RECONCILIATION/TERMINAL_SAFE. Статус: OPEN_P0=0, OPEN_P1=0, OPEN_P2=0; production code отсутствует; real trading запрещена. > **Граница реализации HSB.1V (2026-08-10).** Описанный production lifecycle остаётся нормативной спецификацией, а не реализованным сценарием. В каркасе нет production execution, broker-money runtime и production persistence. Действуют: ровно один Far; promotion только из actual BigCore residual; FinalReserve запрещён для Partial Far; allocations не прибавляются к actual money повторно; Final Close определяется только actual money; только COMPLETED_FILL снимает transaction barrier; retry сохраняет ActionID; conflict ведёт в RECONCILING; unresolved critical error — в TERMINAL_SAFE; no auto-resume; REAL_LIMITED и HSB.2 запрещены.","UNIMPLEMENTED",@J4,@J5,@J6)],"Rows":[@T2("DOC-00-L7-1",@J23,7,"Назначение и область",@SOURCE_LINE(@J23,7),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@ROWS(lines=[11..19],ordinals=2..10,template={"RequirementID":ID("DOC-00",line,ordinal),"SourceFile":@J23,"Line":line,"Section":"Требования","Text":@SOURCE_LINE(@J23,line),"CodeOwner":@J24,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@T2("DOC-00-L23-11",@J23,23,@J26,@SOURCE_LINE(@J23,23),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-00-L27-12",@J23,27,"Запрещённые состояния и error route",@SOURCE_LINE(@J23,27),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-00-L31-13",@J23,31,"Restart, owner, тесты",@SOURCE_LINE(@J23,31),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-01-L7-14",@J27,7,"Назначение",@SOURCE_LINE(@J27,7),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@ROWS(lines=[11,13..27],ordinals=15..30,template={"RequirementID":ID("DOC-01",line,ordinal),"SourceFile":@J27,"Line":line,"Section":"Основные типы","Text":@SOURCE_LINE(@J27,line),"CodeOwner":@J24,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[31..34],ordinals=31..34,template={"RequirementID":ID("DOC-01",line,ordinal),"SourceFile":@J27,"Line":line,"Section":"Projected и actual","Text":@SOURCE_LINE(@J27,line),"CodeOwner":@J24,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@T2("DOC-01-L38-35",@J27,38,"Знаки",@SOURCE_LINE(@J27,38),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-01-L42-36",@J27,42,"Округление",@SOURCE_LINE(@J27,42),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@ROWS(lines=[46..52],ordinals=37..43,template={"RequirementID":ID("DOC-01",line,ordinal),"SourceFile":@J27,"Line":line,"Section":"Запрет смешения","Text":@SOURCE_LINE(@J27,line),"CodeOwner":@J24,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@T2("DOC-01-L56-44",@J27,56,"Контракт",@SOURCE_LINE(@J27,56),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@ROWS(lines=[7,9..16],ordinals=45..53,template={"RequirementID":ID("DOC-02",line,ordinal),"SourceFile":@J28,"Line":line,"Section":"Роли","Text":@SOURCE_LINE(@J28,line),"CodeOwner":@J24,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[20..21,23..28],ordinals=54..61,template={"RequirementID":ID("DOC-02",line,ordinal),"SourceFile":@J28,"Line":line,"Section":"Identity tuple","Text":@SOURCE_LINE(@J28,line),"CodeOwner":@J24,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@T2("DOC-02-L32-62",@J28,32,@J26,@SOURCE_LINE(@J28,32),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-02-L36-63",@J28,36,"Restart и errors",@SOURCE_LINE(@J28,36),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L6-64",@J2,6,"Полный цикл",@SOURCE_LINE(@J2,6),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L9-65",@J2,9,"Роли и направления",@SOURCE_LINE(@J2,9),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L12-66",@J2,12,"Объёмы и три закона",@SOURCE_LINE(@J2,12),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L15-67",@J2,15,"Typed control prices",@SOURCE_LINE(@J2,15),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L18-68",@J2,18,@J10,@SOURCE_LINE(@J2,18),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L21-69",@J2,21,"NewFar",@SOURCE_LINE(@J2,21),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L24-70",@J2,24,"Money и allocation",@SOURCE_LINE(@J2,24),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L27-71",@J2,27,"Partial Far",@SOURCE_LINE(@J2,27),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L30-72",@J2,30,"Transition Loss",@SOURCE_LINE(@J2,30),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L33-73",@J2,33,"Final Close",@SOURCE_LINE(@J2,33),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L36-74",@J2,36,"Small confirmation",@SOURCE_LINE(@J2,36),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L39-75",@J2,39,@J18,@SOURCE_LINE(@J2,39),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L42-76",@J2,42,"Risk, margin и emergency",@SOURCE_LINE(@J2,42),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L45-77",@J2,45,@J21,@SOURCE_LINE(@J2,45),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L48-78",@J2,48,"Restart/error semantics",@SOURCE_LINE(@J2,48),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-03-L50-79",@J2,50,"Restart/error semantics",@SOURCE_LINE(@J2,50),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L6-80",@J29,6,"Размерности",@SOURCE_LINE(@J29,6),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L9-81",@J29,9,"Объёмы",@SOURCE_LINE(@J29,9),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L12-82",@J29,12,"Recovery slope",@SOURCE_LINE(@J29,12),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L15-83",@J29,15,"Reserve Catch-Up",@SOURCE_LINE(@J29,15),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L18-84",@J29,18,"RecoveryPL",@SOURCE_LINE(@J29,18),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L21-85",@J29,21,"Compression",@SOURCE_LINE(@J29,21),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L24-86",@J29,24,"Transition Loss",@SOURCE_LINE(@J29,24),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L27-87",@J29,27,"Final Close",@SOURCE_LINE(@J29,27),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L30-88",@J29,30,"Allocation conservation",@SOURCE_LINE(@J29,30),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L33-89",@J29,33,"Future Small",@SOURCE_LINE(@J29,33),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L36-90",@J29,36,"Дискретная конечность",@SOURCE_LINE(@J29,36),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L39-91",@J29,39,"Направления",@SOURCE_LINE(@J29,39),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-04-L42-92",@J29,42,"Fail-closed",@SOURCE_LINE(@J29,42),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@ROWS(lines=[6..13],ordinals=93..100,template={"RequirementID":ID("DOC-05",line,ordinal),"SourceFile":@J31,"Line":line,"Section":"Typed control prices","Text":@SOURCE_LINE(@J31,line),"CodeOwner":@J30,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@T2("DOC-05-L16-101",@J31,16,"Broker grid",@SOURCE_LINE(@J31,16),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-05-L19-102",@J31,19,"Big levels",@SOURCE_LINE(@J31,19),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-05-L22-103",@J31,22,"Control proof range",@SOURCE_LINE(@J31,22),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-05-L25-104",@J31,25,"Small confirmation",@SOURCE_LINE(@J31,25),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-05-L28-105",@J31,28,"Initial geometry",@SOURCE_LINE(@J31,28),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-05-L31-106",@J31,31,"Error/restart",@SOURCE_LINE(@J31,31),@J30,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-06-L6-107",@J32,6,"Состояния",@SOURCE_LINE(@J32,6),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-06-L9-108",@J32,9,"Главный инвариант",@SOURCE_LINE(@J32,9),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-06-L12-109",@J32,12,"Переход action",@SOURCE_LINE(@J32,12),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-06-L15-110",@J32,15,"Small",@SOURCE_LINE(@J32,15),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-06-L18-111",@J32,18,"Emergency",@SOURCE_LINE(@J32,18),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-06-L21-112",@J32,21,"Restart",@SOURCE_LINE(@J32,21),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-07-L6-113",@J33,6,"Цепочка",@SOURCE_LINE(@J33,6),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-07-L9-114",@J33,9,"Идентификаторы",@SOURCE_LINE(@J33,9),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-07-L12-115",@J33,12,"OwnershipGuard",@SOURCE_LINE(@J33,12),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-07-L15-116",@J33,15,"Outcomes",@SOURCE_LINE(@J33,15),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-07-L18-117",@J33,18,"Retry",@SOURCE_LINE(@J33,18),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-07-L21-118",@J33,21,"Timeout/delayed events",@SOURCE_LINE(@J33,21),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-07-L24-119",@J33,24,"Restart",@SOURCE_LINE(@J33,24),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-08-L6-120",@J34,6,"DealNet",@SOURCE_LINE(@J34,6),@J35,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-08-L9-121",@J34,9,"Economic Ledger",@SOURCE_LINE(@J34,9),@J35,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-08-L12-122",@J34,12,"Allocation Ledger",@SOURCE_LINE(@J34,12),@J35,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-08-L15-123",@J34,15,"Keys/exactly-once",@SOURCE_LINE(@J34,15),@J35,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-08-L18-124",@J34,18,"Isolation",@SOURCE_LINE(@J34,18),@J35,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-08-L21-125",@J34,21,"Transition и Final Close",@SOURCE_LINE(@J34,21),@J35,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-08-L24-126",@J34,24,"Reservation/restart",@SOURCE_LINE(@J34,24),@J35,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-09-L6-127",@J36,6,"Identity и scope",@SOURCE_LINE(@J36,6),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@ROWS(lines=[9..17],ordinals=128..136,template={"RequirementID":ID("DOC-09",line,ordinal),"SourceFile":@J36,"Line":line,"Section":"Последовательность","Text":@SOURCE_LINE(@J36,line),"CodeOwner":@J24,"Status":"UNIMPLEMENTED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@T2("DOC-09-L20-137",@J36,20,"Exclusion",@SOURCE_LINE(@J36,20),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-09-L23-138",@J36,23,"Retry/timeout",@SOURCE_LINE(@J36,23),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-09-L26-139",@J36,26,"Restart/error",@SOURCE_LINE(@J36,26),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-09-L28-140",@J36,28,"Restart/error",@SOURCE_LINE(@J36,28),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@ROWS(lines=[5,7,9,11,13,15,17],ordinals=141..147,template={"RequirementID":ID("DOC-10",line,ordinal),"SourceFile":@J37,"Line":line,"Section":@J38,"Text":@SOURCE_LINE(@J37,line),"CodeOwner":@J24,"Status":"UNIMPLEMENTED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[5,7,9,11,13],ordinals=148..152,template={"RequirementID":ID("DOC-11",line,ordinal),"SourceFile":@J39,"Line":line,"Section":"11. Partial Far","Text":@SOURCE_LINE(@J39,line),"CodeOwner":@J24,"Status":"UNIMPLEMENTED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[5,7,9,11,13,15,17],ordinals=153..159,template={"RequirementID":ID("DOC-12",line,ordinal),"SourceFile":@J40,"Line":line,"Section":@J41,"Text":@SOURCE_LINE(@J40,line),"CodeOwner":@J24,"Status":"UNIMPLEMENTED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@T2("DOC-13-L6-160",@J42,6,"Trigger confirmation",@SOURCE_LINE(@J42,6),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-13-L9-161",@J42,9,"Immutable plan и loss caps",@SOURCE_LINE(@J42,9),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-13-L12-162",@J42,12,"Единственный порядок",@SOURCE_LINE(@J42,12),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-13-L14-163",@J42,14,"Единственный порядок",@SOURCE_LINE(@J42,14),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-13-L17-164",@J42,17,"Инварианты",@SOURCE_LINE(@J42,17),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-13-L20-165",@J42,20,"Restart/error",@SOURCE_LINE(@J42,20),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-13-L22-166",@J42,22,"Restart/error",@SOURCE_LINE(@J42,22),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-14-L6-167",@J43,6,"Входы",@SOURCE_LINE(@J43,6),@J30,"CONTRADICTORY",@J25,"Primary owner reading"),@ROWS(lines=[9..23,25,27],ordinals=168..184,template={"RequirementID":ID("DOC-14",line,ordinal),"SourceFile":@J43,"Line":line,"Section":"Алгоритм","Text":@SOURCE_LINE(@J43,line),"CodeOwner":@J30,"Status":"CONTRADICTORY","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@T2("DOC-15-L6-185",@J44,6,"Configurable limits",@SOURCE_LINE(@J44,6),@J24,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-15-L9-186",@J44,9,"Gate order",@SOURCE_LINE(@J44,9),@J24,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-15-L12-187",@J44,12,"Risk money",@SOURCE_LINE(@J44,12),@J24,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-15-L15-188",@J44,15,"Transition caps",@SOURCE_LINE(@J44,15),@J24,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-15-L18-189",@J44,18,"Emergency",@SOURCE_LINE(@J44,18),@J24,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-15-L21-190",@J44,21,"REAL_LIMITED",@SOURCE_LINE(@J44,21),@J24,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-15-L23-191",@J44,23,"REAL_LIMITED",@SOURCE_LINE(@J44,23),@J24,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-16-L6-192",@J45,6,"Backend",@SOURCE_LINE(@J45,6),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-16-L9-193",@J45,9,"Snapshot",@SOURCE_LINE(@J45,9),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-16-L12-194",@J45,12,"Canonical commit",@SOURCE_LINE(@J45,12),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-16-L15-195",@J45,15,"Restart",@SOURCE_LINE(@J45,15),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-16-L18-196",@J45,18,"Corruption",@SOURCE_LINE(@J45,18),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@T2("DOC-16-L20-197",@J45,20,"Corruption",@SOURCE_LINE(@J45,20),@J24,"UNIMPLEMENTED",@J25,"Primary owner reading"),@ROWS(lines=[5,7,9],ordinals=198..200,template={"RequirementID":ID("DOC-17",line,ordinal),"SourceFile":@J46,"Line":line,"Section":@J47,"Text":@SOURCE_LINE(@J46,line),"CodeOwner":@J24,"Status":"UNIMPLEMENTED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[12..21,23,25],ordinals=201..212,template={"RequirementID":ID("DOC-17",line,ordinal),"SourceFile":@J46,"Line":line,"Section":"Обязательные routes","Text":@SOURCE_LINE(@J46,line),"CodeOwner":@J24,"Status":"UNIMPLEMENTED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@T2("DOC-18-L6-213",@J48,6,"Слои",@SOURCE_LINE(@J48,6),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@ROWS(lines=[9,11..24],ordinals=214..228,template={"RequirementID":ID("DOC-18",line,ordinal),"SourceFile":@J48,"Line":line,"Section":"Decision mapping","Text":@SOURCE_LINE(@J48,line),"CodeOwner":@J24,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@T2("DOC-18-L27-229",@J48,27,"Dependency rules",@SOURCE_LINE(@J48,27),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-18-L29-230",@J48,29,"Dependency rules",@SOURCE_LINE(@J48,29),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@ROWS(lines=[1..19],ordinals=231..249,template={"RequirementID":ID("DOC-19",line,ordinal),"SourceFile":@J49,"Line":line,"Section":"","Text":@SOURCE_LINE(@J49,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@ROWS(lines=[25,27..42],ordinals=250..266,template={"RequirementID":ID("DOC-19",line,ordinal),"SourceFile":@J49,"Line":line,"Section":@J64,"Text":@SOURCE_LINE(@J49,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@ROWS(lines=[47..55,58],ordinals=267..276,template={"RequirementID":ID("DOC-19",line,ordinal),"SourceFile":@J49,"Line":line,"Section":"Итог","Text":@SOURCE_LINE(@J49,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@ROWS(lines=[62..73,76],ordinals=277..289,template={"RequirementID":ID("DOC-19",line,ordinal),"SourceFile":@J49,"Line":line,"Section":@J70,"Text":@SOURCE_LINE(@J49,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@T2("DOC-19-L80-290",@J49,80,"Правило статуса HSB.1V",@SOURCE_LINE(@J49,80),@J24,"UNTESTED",@J25,@J51),@ROWS(lines=[87..99,102],ordinals=291..304,template={"RequirementID":ID("DOC-19",line,ordinal),"SourceFile":@J49,"Line":line,"Section":@J76,"Text":@SOURCE_LINE(@J49,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@ROWS(lines=[106,108..117,119],ordinals=305..316,template={"RequirementID":ID("DOC-19",line,ordinal),"SourceFile":@J49,"Line":line,"Section":"HSB.2A — расчётные модули","Text":@SOURCE_LINE(@J49,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@ROWS(lines=[123,125..138,140],ordinals=317..332,template={"RequirementID":ID("DOC-19",line,ordinal),"SourceFile":@J49,"Line":line,"Section":@J79,"Text":@SOURCE_LINE(@J49,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@ROWS(lines=[144,146..155,157],ordinals=333..344,template={"RequirementID":ID("DOC-19",line,ordinal),"SourceFile":@J49,"Line":line,"Section":@J80,"Text":@SOURCE_LINE(@J49,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@ROWS(lines=[161,163..169,171],ordinals=345..353,template={"RequirementID":ID("DOC-19",line,ordinal),"SourceFile":@J49,"Line":line,"Section":@J82,"Text":@SOURCE_LINE(@J49,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@ROWS(lines=[175,177..182,184],ordinals=354..361,template={"RequirementID":ID("DOC-19",line,ordinal),"SourceFile":@J49,"Line":line,"Section":@J83,"Text":@SOURCE_LINE(@J49,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@T2("DOC-19-L188-362",@J49,188,"HSB.2C — static orchestration",@SOURCE_LINE(@J49,188),@J24,"UNTESTED",@J25,@J51),@ROWS(lines=[192,194..223,225..257,259..296,298..316,318..336,338..360,362..380,382..403,405..418],ordinals=363..580,template={"RequirementID":ID("DOC-19",line,ordinal),"SourceFile":@J49,"Line":line,"Section":"HSB.2C-R1","Text":@SOURCE_LINE(@J49,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@T2("DOC-19-L422-581",@J49,422,"HSB.2E-PREP-R4-R9-R4A-R8",@SOURCE_LINE(@J49,422),@J24,"UNTESTED",@J25,@J51),@T2("DOC-19-L426-582",@J49,426,"HSB.2E-PREP-R4-R9-R4A-R9",@SOURCE_LINE(@J49,426),@J24,"UNTESTED",@J25,@J51),@T2("DOC-19-L430-583",@J49,430,"HSB.2E-PREP-R4-R9-R4A-R10",@SOURCE_LINE(@J49,430),@J24,"UNTESTED",@J25,@J51),@T2("DOC-19-L434-584",@J49,434,"HSB.2E-PREP-R4-R9-R4A-R11",@SOURCE_LINE(@J49,434),@J24,"UNTESTED",@J25,@J51),@T2("DOC-20-L7-585","Docs/20_TEST_STRATEGY_RU.md",7,"Unit MQL5",@SOURCE_LINE("Docs/20_TEST_STRATEGY_RU.md",7),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-20-L11-586","Docs/20_TEST_STRATEGY_RU.md",11,"Integration MQL5",@SOURCE_LINE("Docs/20_TEST_STRATEGY_RU.md",11),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@T2("DOC-20-L15-587","Docs/20_TEST_STRATEGY_RU.md",15,"Strategy Tester",@SOURCE_LINE("Docs/20_TEST_STRATEGY_RU.md",15),@J24,"PARTIALLY_VERIFIED",@J25,"Primary owner reading"),@ROWS(lines=[19,21..26,28],ordinals=588..595,template={"RequirementID":ID("DOC-20",line,ordinal),"SourceFile":"Docs/20_TEST_STRATEGY_RU.md","Line":line,"Section":"Evidence","Text":@SOURCE_LINE("Docs/20_TEST_STRATEGY_RU.md",line),"CodeOwner":@J24,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[1..19],ordinals=596..614,template={"RequirementID":ID("DOC-21",line,ordinal),"SourceFile":@J199,"Line":line,"Section":"","Text":@SOURCE_LINE(@J199,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@T2("DOC-21-L25-615",@J199,25,@J200,@SOURCE_LINE(@J199,25),@J24,"UNTESTED",@J25,@J51),@T2("DOC-21-L27-616",@J199,27,@J200,@SOURCE_LINE(@J199,27),@J24,"UNTESTED",@J25,@J51),@ROWS(lines=[31..42,45],ordinals=617..629,template={"RequirementID":ID("DOC-21",line,ordinal),"SourceFile":@J199,"Line":line,"Section":@J70,"Text":@SOURCE_LINE(@J199,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@ROWS(lines=[52..64,67,69..98,100..132,134..171,173..191,193..211,213..235,237..255,257..278,280..293],ordinals=630..860,template={"RequirementID":ID("DOC-21",line,ordinal),"SourceFile":@J199,"Line":line,"Section":@J76,"Text":@SOURCE_LINE(@J199,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@T2("DOC-21-L297-861",@J199,297,"HSB.2E-PREP-R4-R9-R4A-R8",@SOURCE_LINE(@J199,297),@J24,"UNTESTED",@J25,@J51),@T2("DOC-21-L301-862",@J199,301,"HSB.2E-PREP-R4-R9-R4A-R9",@SOURCE_LINE(@J199,301),@J24,"UNTESTED",@J25,@J51),@T2("DOC-21-L305-863",@J199,305,"HSB.2E-PREP-R4-R9-R4A-R10",@SOURCE_LINE(@J199,305),@J24,"UNTESTED",@J25,@J51),@T2("DOC-21-L309-864",@J199,309,"HSB.2E-PREP-R4-R9-R4A-R11",@SOURCE_LINE(@J199,309),@J24,"UNTESTED",@J25,@J51),@ROWS(lines=[1..19],ordinals=865..883,template={"RequirementID":ID("DOC-22",line,ordinal),"SourceFile":@J201,"Line":line,"Section":"","Text":@SOURCE_LINE(@J201,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@ROWS(lines=[23..41,43],ordinals=884..903,template={"RequirementID":ID("DOC-22",line,ordinal),"SourceFile":@J201,"Line":line,"Section":@J202,"Text":@SOURCE_LINE(@J201,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@ROWS(lines=[47..58,61],ordinals=904..916,template={"RequirementID":ID("DOC-22",line,ordinal),"SourceFile":@J201,"Line":line,"Section":@J70,"Text":@SOURCE_LINE(@J201,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@ROWS(lines=[68..80,83,85..114,116..148,150..187,189..207,209..227,229..251,253..271,273..294,296..309],ordinals=917..1147,template={"RequirementID":ID("DOC-22",line,ordinal),"SourceFile":@J201,"Line":line,"Section":@J76,"Text":@SOURCE_LINE(@J201,line),"CodeOwner":@J24,"Status":"UNTESTED","Evidence":@J25,"ReviewBoundary":@J51}),@T2("DOC-22-L313-1148",@J201,313,"HSB.2E-PREP-R4-R9-R4A-R8",@SOURCE_LINE(@J201,313),@J24,"UNTESTED",@J25,@J51),@T2("DOC-22-L317-1149",@J201,317,"HSB.2E-PREP-R4-R9-R4A-R9",@SOURCE_LINE(@J201,317),@J24,"UNTESTED",@J25,@J51),@T2("DOC-22-L321-1150",@J201,321,"HSB.2E-PREP-R4-R9-R4A-R10",@SOURCE_LINE(@J201,321),@J24,"UNTESTED",@J25,@J51),@T2("DOC-22-L325-1151",@J201,325,"HSB.2E-PREP-R4-R9-R4A-R11",@SOURCE_LINE(@J201,325),@J24,"UNTESTED",@J25,@J51),@ROWS(lines=[4..7,9,11,13..26,28],ordinals=1152..1172,template={"RequirementID":ID("DOC-23",line,ordinal),"SourceFile":@J203,"Line":line,"Section":@J204,"Text":@SOURCE_LINE(@J203,line),"CodeOwner":@J24,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[3,5,7,9,11,14..20],ordinals=1173..1184,template={"RequirementID":ID("DOC-24",line,ordinal),"SourceFile":@J205,"Line":line,"Section":@J206,"Text":@SOURCE_LINE(@J205,line),"CodeOwner":@J35,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[3,5,7,10..16],ordinals=1185..1194,template={"RequirementID":ID("DOC-25",line,ordinal),"SourceFile":@J212,"Line":line,"Section":@J213,"Text":@SOURCE_LINE(@J212,line),"CodeOwner":@J24,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[3,5,7,10..16],ordinals=1195..1204,template={"RequirementID":ID("DOC-26",line,ordinal),"SourceFile":@J214,"Line":line,"Section":"26. Geometry Engine HSB.2A","Text":@SOURCE_LINE(@J214,line),"CodeOwner":@J24,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[3,5,7,10..16],ordinals=1205..1214,template={"RequirementID":ID("DOC-27",line,ordinal),"SourceFile":@J215,"Line":line,"Section":@J216,"Text":@SOURCE_LINE(@J215,line),"CodeOwner":@J30,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[3,5,7,10..14],ordinals=1215..1222,template={"RequirementID":ID("DOC-27",line,ordinal),"SourceFile":@J217,"Line":line,"Section":@J218,"Text":@SOURCE_LINE(@J217,line),"CodeOwner":@J30,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[19,21,24..30],ordinals=1223..1231,template={"RequirementID":ID("DOC-27",line,ordinal),"SourceFile":@J217,"Line":line,"Section":"Коррекция HSB.2B-R","Text":@SOURCE_LINE(@J217,line),"CodeOwner":@J30,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[35,37,39,41],ordinals=1232..1235,template={"RequirementID":ID("DOC-27",line,ordinal),"SourceFile":@J217,"Line":line,"Section":"Коррекция HSB.2B-R2","Text":@SOURCE_LINE(@J217,line),"CodeOwner":@J30,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[3,5,7,10..14],ordinals=1236..1243,template={"RequirementID":ID("DOC-28",line,ordinal),"SourceFile":@J225,"Line":line,"Section":"28. NewFar Solver HSB.2B","Text":@SOURCE_LINE(@J225,line),"CodeOwner":@J30,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[19,21,24..30],ordinals=1244..1252,template={"RequirementID":ID("DOC-28",line,ordinal),"SourceFile":@J225,"Line":line,"Section":"Коррекция HSB.2B-R","Text":@SOURCE_LINE(@J225,line),"CodeOwner":@J30,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[35,37,39],ordinals=1253..1255,template={"RequirementID":ID("DOC-28",line,ordinal),"SourceFile":@J225,"Line":line,"Section":"Коррекция HSB.2B-R2","Text":@SOURCE_LINE(@J225,line),"CodeOwner":@J30,"Status":"PARTIALLY_VERIFIED","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[3,5,7,10..14],ordinals=1256..1263,template={"RequirementID":ID("DOC-29",line,ordinal),"SourceFile":@J226,"Line":line,"Section":@J227,"Text":@SOURCE_LINE(@J226,line),"CodeOwner":@J30,"Status":"CONTRADICTORY","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[19,21,24..30],ordinals=1264..1272,template={"RequirementID":ID("DOC-29",line,ordinal),"SourceFile":@J226,"Line":line,"Section":"Коррекция HSB.2B-R","Text":@SOURCE_LINE(@J226,line),"CodeOwner":@J30,"Status":"CONTRADICTORY","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@T2("DOC-29-L35-1273",@J226,35,"Коррекция HSB.2B-R2",@SOURCE_LINE(@J226,35),@J30,"CONTRADICTORY",@J25,"Primary owner reading"),@T2("DOC-29-L37-1274",@J226,37,"Коррекция HSB.2B-R2",@SOURCE_LINE(@J226,37),@J30,"CONTRADICTORY",@J25,"Primary owner reading"),@ROWS(lines=[3,5,7,10..14],ordinals=1275..1282,template={"RequirementID":ID("DOC-30",line,ordinal),"SourceFile":@J228,"Line":line,"Section":@J229,"Text":@SOURCE_LINE(@J228,line),"CodeOwner":@J30,"Status":"CONTRADICTORY","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[3,5,7],ordinals=1283..1285,template={"RequirementID":ID("DOC-31",line,ordinal),"SourceFile":@J230,"Line":line,"Section":@J231,"Text":@SOURCE_LINE(@J230,line),"CodeOwner":@J35,"Status":"CONTRADICTORY","Evidence":@J25,"ReviewBoundary":"Primary owner reading"}),@ROWS(lines=[3,5,7],ordinals=1286..1288,template={"RequirementID":ID("DOC-32",line,ordinal),"SourceFile":@J232,"Line":line,"Section":@J233,"Text":@SOURCE_LINE(@J232,line),"CodeOwner":@J35,"Status":"CONTRADICTORY","Evidence":@J25,"ReviewBoundary":"Primary owner reading"})],"CodeToRequirement":[@T3(@J234,"OnInit",19,@J235,true,["HSBI_BuildRuntimePolicy","HSBI_InitializeContext",@J236,"HSBI_Log"],[],"NOT_RUN",@J237),@T3(@J234,"OnDeinit",29,@J235,true,["HSBI_Log"],[],"NOT_RUN",@J237),@T3(@J234,"OnTick",35,@J235,true,["HSBI_SubmitActionStub"],["FSA-014"],"NOT_RUN",@J237),@T3(@J234,"OnTimer",41,@J235,true,[@J238],[],"NOT_RUN",@J237),@T3(@J239,"HSBI_InitializeContext",8,@J24,true,[],[],"NOT_RUN",@J237),@T3(@J239,"HSBI_ResetContext",9,@J24,false,["HSBI_InitializeContext"],[],"NOT_RUN",@J237),@T3(@J239,"HSBI_ContextPositionValid",10,@J24,false,["HSBI_IsKnownRole"],[],"NOT_RUN",@J237),@T3(@J239,"HSBI_ContextRolesConflict",19,@J24,false,[],[],"NOT_RUN",@J237),@T3(@J239,"HSBI_ContextPositionInScope",27,@J24,false,["HSBI_IsValidIdentity"],[],"NOT_RUN",@J237),@T3(@J239,"HSBI_ValidateContext",33,@J24,false,["HSBI_BuildRuntimePolicy","HSBI_ContextPositionInScope","HSBI_ContextPositionValid","HSBI_ContextRolesConflict",@J240],["FSA-009"],"NOT_RUN",@J237),@T3(@J241,"HSBI_IsValidIdentity",6,@J24,false,[],[],"NOT_RUN",@J237),@T3(@J241,"HSBI_SameCycle",7,@J24,false,[],[],"NOT_RUN",@J237),@T3(@J241,"HSBI_SamePositionOwner",8,@J24,false,["HSBI_SameCycle"],[],"NOT_RUN",@J237),@T3(@J241,"HSBI_SameSymbolScope",9,@J24,false,[],[],"NOT_RUN",@J237),@T3(@J241,"HSBI_UlongToString",10,@J24,false,[],[],"NOT_RUN",@J237),@T3(@J241,"HSBI_SerializeIdentity",23,@J24,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J242,"HSBI_ExactlyOneFarOrZero",5,@J24,false,["HSBI_CountFarRoles","HSBI_Result"],[],"NOT_RUN",@J237),@T3(@J242,"HSBI_NoDualTail",6,@J24,false,["HSBI_ExactlyOneFarOrZero"],[],"NOT_RUN",@J237),@T3(@J242,"HSBI_NoUnknownRole",7,@J24,false,@J243,[],"NOT_RUN",@J237),@T3(@J242,@J244,8,@J24,false,["HSBI_Result"],[],"NOT_RUN",@J237),@T3(@J242,"HSBI_StateRevisionMonotonic",9,@J24,false,["HSBI_Result"],[],"NOT_RUN",@J237),@T3(@J242,@J245,10,@J24,false,["HSBI_Result"],[],"NOT_RUN",@J237),@T3(@J242,@J246,11,@J24,false,["HSBI_Result"],[],"NOT_RUN",@J237),@T3(@J242,"HSBI_AllocationConservation",12,@J24,false,["HSBI_Result"],[],"NOT_RUN",@J237),@T3(@J242,@J247,13,@J24,false,["HSBI_Result"],[],"NOT_RUN",@J237),@T3(@J248,"HSBI_ReasonToString",4,@J24,true,[],[],"NOT_RUN",@J237),@T3("Include/Core/HSBI_Roles.mqh","HSBI_IsKnownRole",6,@J24,false,[],[],"NOT_RUN",@J237),@T3("Include/Core/HSBI_Roles.mqh",@J249,7,@J24,false,@J243,[],"NOT_RUN",@J237),@T3("Include/Core/HSBI_Roles.mqh","HSBI_CanPromoteToFar",8,@J24,false,[],[],"NOT_RUN",@J237),@T3("Include/Core/HSBI_Roles.mqh","HSBI_ValidateRoleTransition",9,@J24,false,[],[],"NOT_RUN",@J237),@T3("Include/Core/HSBI_Roles.mqh","HSBI_CountFarRoles",10,@J24,true,[],[],"NOT_RUN",@J237),@T3(@J250,@J240,5,@J24,false,[],[],"NOT_RUN",@J237),@T3(@J251,"HSBI_BuildRuntimePolicy",12,@J24,true,[],[],"NOT_RUN",@J237),@T3(@J251,"HSBI_IsInjectedProofAllowed",23,@J24,false,["HSBI_BuildRuntimePolicy"],[],"NOT_RUN",@J237),@T3(@J251,@J252,24,@J24,false,["HSBI_BuildRuntimePolicy"],[],"NOT_RUN",@J237),@T3(@J251,@J236,25,@J24,true,[],[],"NOT_RUN",@J237),@T3(@J251,@J253,26,@J24,false,["HSBI_BuildRuntimePolicy"],[],"NOT_RUN",@J237),@T3(@J251,@J254,28,@J24,false,["HSBI_BuildRuntimePolicy"],[],"NOT_RUN",@J237),@T3(@J255,"HSBI_IsTransitionAllowed",5,@J24,false,[],["FSA-012"],"NOT_RUN",@J237),@T3(@J255,"HSBI_ProposeStateTransition",6,@J24,false,["HSBI_IsTransitionAllowed"],["FSA-022"],"NOT_RUN",@J237),@T3(@J255,@J256,7,@J24,false,["HSBI_ProposeStateTransition"],[],"NOT_RUN",@J237),@T3(@J255,"HSBI_ConflictTargetState",8,@J24,false,[],[],"NOT_RUN",@J237),@T3(@J255,@J257,9,@J24,false,[],[],"NOT_RUN",@J237),@T3(@J255,@J258,10,@J24,false,[],[],"NOT_RUN",@J237),@T3(@J259,"HSBI_ValidateStateTopology",4,@J24,false,["HSBI_Result"],[],"NOT_RUN",@J237),@T3(@J259,"HSBI_OutcomeCompletesAction",5,@J24,false,[],[],"NOT_RUN",@J237),@T3("Include/Core/HSBI_Types.mqh","HSBI_Result",7,@J24,false,[],[],"NOT_RUN",@J237),@T3(@J260,@J261,5,@J235,true,["HSBI_CountFarRoles"],[],"NOT_RUN",@J237),@T3(@J260,@J238,6,@J235,true,[@J261],[],"NOT_RUN",@J237),@T3(@J262,"HSBI_Log",6,@J235,true,["HSBI_ReasonToString"],[],"NOT_RUN",@J237),@T3(@J263,"HSBI_BuildPanelModel",5,@J235,false,["HSBI_ReasonToString","HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J264,"HSBI_ValidateActionRecord",6,@J33,false,[],[],"NOT_RUN",@J237),@T3(@J264,"HSBI_SerializeActionIds",7,@J33,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J265,"HSBI_ValidateEventRecord",6,@J33,false,[],[],"NOT_RUN",@J237),@T3(@J265,"HSBI_SerializeEventIds",7,@J33,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J266,"HSBI_ExecutionIntentDigest",15,@J33,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J266,@J267,26,@J33,false,["HSBI_ExecutionIntentDigest"],[],"NOT_RUN",@J237),@T3(@J266,"HSBI_IsValidIntentStatus",27,@J33,false,[],[],"NOT_RUN",@J237),@T3(@J266,@J268,28,@J33,false,["HSBI_IsFiniteNumber","HSBI_IsValidIntentStatus",@J267],[],"NOT_RUN",@J237),@T3(@J266,"HSBI_IntentIdempotencyKey",42,@J33,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J266,"HSBI_IsSameIntentRetry",43,@J33,false,["HSBI_IntentIdempotencyKey"],[],"NOT_RUN",@J237),@T3(@J266,"HSBI_IsIntentConflict",44,@J33,false,["HSBI_IntentIdempotencyKey"],[],"NOT_RUN",@J237),@T3(@J269,@J270,17,@J33,false,["HSBI_GridTolerance",@J252,@J271,@J267,@J268,@J272,"HSBI_ValidateVolume"],[],"NOT_RUN",@J237),@T3(@J269,@J273,35,@J33,false,[],[],"NOT_RUN",@J237),@T3(@J269,"HSBI_IntentRetryAllowed",47,@J33,false,[],[],"NOT_RUN",@J237),@T3(@J274,"HSBI_ExternalOutcomeDigest",13,@J33,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J274,@J275,22,@J33,false,["HSBI_ExternalOutcomeDigest",@J254,@J267],[],"NOT_RUN",@J237),@T3(@J276,"HSBI_SubmitActionStub",5,@J33,true,[],[],"NOT_RUN",@J237),@T3(@J276,"HSBI_OpenPositionStub",6,@J33,false,["HSBI_SubmitActionStub"],[],"NOT_RUN",@J237),@T3(@J276,"HSBI_ClosePositionStub",7,@J33,false,["HSBI_SubmitActionStub"],[],"NOT_RUN",@J237),@T3(@J276,"HSBI_PartialCloseStub",8,@J33,false,["HSBI_SubmitActionStub"],[],"NOT_RUN",@J237),@T3(@J277,"HSBI_EvaluateOwnership",8,@J33,false,["HSBI_SamePositionOwner"],[],"NOT_RUN",@J237),@T3(@J277,@J278,9,@J33,false,["HSBI_SamePositionOwner"],[],"NOT_RUN",@J237),@T3(@J277,@J279,13,@J33,false,[],[],"NOT_RUN",@J237),@T3(@J280,"HSBI_IsCompletedOutcome",6,@J33,false,[],[],"NOT_RUN",@J237),@T3(@J280,"HSBI_IsRetryOfSameAction",7,@J33,false,[],[],"NOT_RUN",@J237),@T3(@J280,"HSBI_IsFreshEvent",8,@J33,false,[],[],"NOT_RUN",@J237),@T3(@J280,@J281,9,@J33,false,["HSBI_IsFreshEvent"],["FSA-006"],"NOT_RUN",@J237),@T3(@J280,"HSBI_RetryAllowed",20,@J33,false,["HSBI_IsRetryOfSameAction"],[],"NOT_RUN",@J237),@T3(@J282,"HSBI_AllocatedTotal",6,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J282,@J283,7,@J35,false,["HSBI_AllocatedTotal"],["FSA-007"],"NOT_RUN",@J237),@T3(@J282,@J284,8,@J35,false,["HSBI_AllocatedTotal"],["FSA-002"],"NOT_RUN",@J237),@T3(@J282,"HSBI_CanConsumeBucket",9,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J282,"HSBI_CanConsumeAmount",10,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J285,@J286,16,@J35,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J285,"HSBI_AllocationPolicyDigest",25,@J35,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J287,"HSBI_BasketLegInput",7,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J287,"HSBI_EvaluateBasketMoney",11,@J35,false,["HSBI_BasketLegInput",@J288,@J289,"HSBI_IsFiniteNumber",@J272],["FSA-029"],"NOT_RUN",@J237),@T3(@J287,"HSBI_BasketMoneyProofDigest",20,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J290,@J291,5,@J35,false,["HSBI_IsFiniteNumber",@J271,"HSBI_ValidatePriceGrid","HSBI_ValidateVolume"],[],"NOT_RUN",@J237),@T3(@J292,"HSBI_MoneyResult",5,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J292,@J293,6,@J35,false,["HSBI_GridTolerance","HSBI_IsFiniteNumber","HSBI_MoneyResult","HSBI_TryProjectedNetMoney",@J271,"HSBI_ValidateCostSnapshot","HSBI_ValidatePriceGrid","HSBI_ValidateVolume"],[],"NOT_RUN",@J237),@T3(@J294,"HSBI_IsFiniteNumber",10,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J294,@J271,11,@J35,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J295,"HSBI_EvaluateCandidateMoney",10,@J35,false,["HSBI_FutureSmallProofDigest","HSBI_SolveFutureSmall"],[],"NOT_RUN",@J237),@T3(@J296,"HSBI_EvaluateCatchUp",4,@J35,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J297,"HSBI_ValidateCostSnapshot",5,@J35,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J297,"HSBI_TryActualDealNet",11,@J35,false,@J298,[],"NOT_RUN",@J237),@T3(@J297,"HSBI_TryProjectedNetMoney",15,@J35,false,@J298,["FSA-019"],"NOT_RUN",@J237),@T3(@J299,"HSBI_BuildSourceDealKey",7,@J35,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J299,"HSBI_ValidateEconomicRecord",8,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J299,"HSBI_SameEconomicRecord",9,@J35,false,[],["FSA-001"],"NOT_RUN",@J237),@T3(@J299,@J300,10,@J35,false,["HSBI_SameEconomicRecord"],[],"NOT_RUN",@J237),@T3(@J299,@J301,11,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J299,"HSBI_IsHarvestSourceEntry",12,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J302,@J288,5,@J35,false,[@J291,"HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J303,@J289,7,@J35,false,[@J293,"HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J304,@J305,10,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J304,@J306,16,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J304,@J307,23,@J35,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J308,"HSBI_ValidateMoneyState",5,@J35,false,[],["FSA-008"],"NOT_RUN",@J237),@T3(@J309,"HSBI_BuildRecoveryPL",9,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J310,@J311,15,@J35,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J310,@J312,25,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J310,@J313,27,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J310,@J314,29,@J35,false,[@J313],[],"NOT_RUN",@J237),@T3(@J310,@J315,31,@J35,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J310,@J316,33,@J35,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J317,@J318,24,@J35,false,@J319,[],"NOT_RUN",@J237),@T3(@J317,"HSBI_ValidateFarLossProof",30,@J35,false,@J319,[],"NOT_RUN",@J237),@T3(@J317,"HSBI_EvaluateReserveCatchUp",35,@J35,false,[@J313,"HSBI_IsFiniteNumber",@J253,@J307,@J315,@J314,@J316,@J286,"HSBI_ValidateFarLossProof",@J311,@J312,@J318],["FSA-003","FSA-004"],"NOT_RUN",@J237),@T3(@J317,"HSBI_ReserveCatchUpDigest",78,@J35,false,[],[],"NOT_RUN",@J237),@T3(@J320,@J321,12,@J322,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J320,"HSBI_ValidateJournalEntry",18,@J322,false,[@J321],[],"NOT_RUN",@J237),@T3(@J320,@J323,21,@J322,false,[],[],"NOT_RUN",@J237),@T3(@J320,"HSBI_IsJournalEntryConflict",23,@J322,false,[],[],"NOT_RUN",@J237),@T3(@J320,"HSBI_ClassifyJournalAppend",25,@J322,false,[@J323,"HSBI_IsJournalEntryConflict","HSBI_ValidateJournalEntry"],["FSA-027"],"NOT_RUN",@J237),@T3(@J320,"HSBI_ValidateJournalChain",31,@J322,false,["HSBI_ValidateJournalEntry"],[],"NOT_RUN",@J237),@T3(@J324,@J325,12,@J322,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J324,@J326,19,@J322,false,[@J268],[],"NOT_RUN",@J237),@T3(@J324,"HSBI_IsActiveIntentStatus",25,@J322,false,[],[],"NOT_RUN",@J237),@T3(@J324,@J327,27,@J322,false,[@J325,"HSBI_IsActiveIntentStatus",@J326],[],"NOT_RUN",@J237),@T3(@J324,"HSBI_RecoverExecutionState",42,@J322,false,[@J327],[],"NOT_RUN",@J237),@T3(@J328,"HSBI_ValidateJournalRecord",6,@J322,false,[],[],"NOT_RUN",@J237),@T3(@J328,"HSBI_SerializeJournalIds",7,@J322,false,["HSBI_SerializeActionIds","HSBI_SerializeEventIds","HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J329,"HSBI_PersistSnapshotStub",7,@J322,false,[],[],"NOT_RUN",@J237),@T3(@J330,"HSBI_CompareReconciliation",7,@J322,false,["HSBI_IsValidIdentity"],[],"NOT_RUN",@J237),@T3(@J331,"HSBI_ValidateSnapshotSchema",8,@J322,false,[],[],"NOT_RUN",@J237),@T3(@J331,"HSBI_TestDigest",9,@J322,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J331,"HSBI_SerializeSnapshotIds",10,@J322,false,["HSBI_SerializeActionIds","HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J332,"HSBI_GridTolerance",7,@J30,false,[],[],"NOT_RUN",@J237),@T3(@J332,"HSBI_IsPriceOnTickGrid",8,@J30,false,@J333,[],"NOT_RUN",@J237),@T3(@J332,"HSBI_NormalizePriceToTick",13,@J30,false,["HSBI_IsFiniteNumber","HSBI_IsPriceOnTickGrid"],[],"NOT_RUN",@J237),@T3(@J332,"HSBI_ValidatePriceGrid",19,@J30,false,["HSBI_IsPriceOnTickGrid",@J271],[],"NOT_RUN",@J237),@T3(@J332,"HSBI_PriceDistanceInTicks",20,@J30,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J332,"HSBI_IsVolumeOnGrid",21,@J30,false,@J333,[],"NOT_RUN",@J237),@T3(@J332,"HSBI_FloorVolumeToStep",26,@J30,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J332,"HSBI_CeilVolumeToStep",27,@J30,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J332,"HSBI_NormalizeVolume",28,@J30,false,["HSBI_CeilVolumeToStep","HSBI_FloorVolumeToStep"],[],"NOT_RUN",@J237),@T3(@J332,"HSBI_ValidateVolume",33,@J30,false,["HSBI_GridTolerance","HSBI_IsFiniteNumber","HSBI_IsVolumeOnGrid",@J271],[],"NOT_RUN",@J237),@T3(@J334,"HSBI_ValidateCandidatePlan",6,@J30,false,["HSBI_IsValidIdentity"],[],"NOT_RUN",@J237),@T3(@J334,@J335,7,@J30,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J334,"HSBI_SameCandidatePlan",8,@J30,false,[@J335],[],"NOT_RUN",@J237),@T3(@J336,"HSBI_IsSnapshotFresh",11,@J30,false,[],["FSA-021"],"NOT_RUN",@J237),@T3(@J336,"HSBI_NormalizePriceToTick",12,@J30,false,[],[],"NOT_RUN",@J237),@T3(@J336,"HSBI_ResolveCloseSide",13,@J30,false,[],[],"NOT_RUN",@J237),@T3(@J336,"HSBI_ValidateMarketSnapshot",14,@J30,false,["HSBI_Result"],[],"NOT_RUN",@J237),@T3(@J336,@J337,15,@J30,false,["HSBI_Result"],[],"NOT_RUN",@J237),@T3(@J336,@J272,16,@J30,false,@J338,[],"NOT_RUN",@J237),@T3(@J339,"HSBI_AggregateDigest",16,@J30,false,[],[],"NOT_RUN",@J237),@T3(@J339,@J340,23,@J30,false,["HSBI_AggregateDigest","HSBI_FutureSmallLevelDigest"],["FSA-015"],"NOT_RUN",@J237),@T3(@J341,@J342,5,@J30,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J341,@J343,12,@J30,false,[],["FSA-018"],"NOT_RUN",@J237),@T3(@J341,"HSBI_ValidateLevelMarket",18,@J30,false,@J338,[],"NOT_RUN",@J237),@T3(@J341,"HSBI_ValidateLevelCosts",27,@J30,false,["HSBI_ValidateCostSnapshot"],[],"NOT_RUN",@J237),@T3(@J341,"HSBI_ValidateFarProjection",32,@J30,false,["HSBI_ValidateVolume"],[],"NOT_RUN",@J237),@T3(@J341,"HSBI_LevelControlPrice",39,@J30,false,[],[],"NOT_RUN",@J237),@T3(@J341,@J344,45,@J30,false,["HSBI_IsInjectedProofAllowed",@J253,@J286,@J271],[],"NOT_RUN",@J237),@T3(@J341,@J345,57,@J30,false,["HSBI_EvaluateBasketMoney",@J346,"HSBI_GridTolerance","HSBI_IsInjectedProofAllowed",@J253,"HSBI_LevelControlPrice","HSBI_SolveBigGeometry","HSBI_ValidateFarProjection","HSBI_ValidateLevelCosts","HSBI_ValidateLevelMarket"],["FSA-017"],"NOT_RUN",@J237),@T3(@J341,"HSBI_FutureSmallLevelDigest",93,@J30,false,["HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J341,"HSBI_FutureSmallProofDigest",106,@J30,false,["HSBI_FutureSmallLevelDigest","HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J341,"HSBI_SolveFutureSmall",113,@J30,false,[@J342,@J345,"HSBI_FutureSmallLevelDigest","HSBI_FutureSmallProofDigest","HSBI_GridTolerance",@J343,@J344],["FSA-028"],"NOT_RUN",@J237),@T3(@J347,"HSBI_ValidateRecoverySlope",6,@J30,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J347,@J348,12,@J30,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J347,"HSBI_SolveBigGeometry",21,@J30,false,["HSBI_CeilVolumeToStep","HSBI_FloorVolumeToStep","HSBI_GridTolerance","HSBI_IsFiniteNumber","HSBI_IsVolumeOnGrid",@J271,"HSBI_ValidateRecoverySlope","HSBI_ValidateVolume"],["FSA-011"],"NOT_RUN",@J237),@T3(@J349,@J350,19,@J30,false,["HSBI_Result"],[],"NOT_RUN",@J237),@T3(@J349,"HSBI_IsCandidateSourceValid",24,@J30,false,[],[],"NOT_RUN",@J237),@T3(@J349,@J351,26,@J30,false,[],[],"NOT_RUN",@J237),@T3(@J349,@J352,33,@J30,false,[@J351],[],"NOT_RUN",@J237),@T3(@J353,@J354,35,@J30,false,["HSBI_AllocationPolicyDigest","HSBI_UlongToString"],["FSA-023"],"NOT_RUN",@J237),@T3(@J353,"HSBI_NewFarInputDigest",47,@J30,false,["HSBI_AllocationPolicyDigest",@J354,@J315,@J316,"HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J353,@J355,59,@J30,false,["HSBI_NewFarInputDigest"],[],"NOT_RUN",@J237),@T3(@J353,"HSBI_ValidateNewFarSource",60,@J30,false,[@J279,"HSBI_SamePositionOwner","HSBI_ValidateVolume"],[],"NOT_RUN",@J237),@T3(@J353,"HSBI_AllowedTransitionLoss",74,@J30,false,[],[],"NOT_RUN",@J237),@T3(@J353,@J356,75,@J30,false,[],[],"NOT_RUN",@J237),@T3(@J353,"HSBI_NewFarProofIdentity",80,@J30,false,[],[],"NOT_RUN",@J237),@T3(@J353,"HSBI_CandidateProofDigest",84,@J30,false,[],[],"NOT_RUN",@J237),@T3(@J353,"HSBI_SolveNewFar",94,@J30,false,[@J340,"HSBI_AllocationPolicyDigest","HSBI_AllowedTransitionLoss",@J356,"HSBI_CandidateProofDigest",@J352,"HSBI_EvaluateCandidateMoney","HSBI_EvaluateNewFarGates","HSBI_EvaluateReserveCatchUp",@J355,@J354,"HSBI_GridTolerance",@J351,"HSBI_IsFiniteNumber",@J253,"HSBI_NewFarInputDigest","HSBI_NewFarProofIdentity","HSBI_NormalizeVolume","HSBI_ReserveCatchUpDigest",@J286,"HSBI_ValidateNewFarSource","HSBI_ValidateVolume"],["FSA-010"],"NOT_RUN",@J237),@T3(@J357,"HSBI_FailClosed",6,@J44,false,[],[],"NOT_RUN",@J237),@T3(@J357,@J358,10,@J44,false,[],[],"NOT_RUN",@J237),@T3(@J359,@J346,29,@J44,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J360,"HSBI_EvaluateNewFarGates",6,@J44,false,["HSBI_IsFiniteNumber"],[],"NOT_RUN",@J237),@T3(@J361,"HSBI_ValidateRiskInput",6,@J44,false,[],["FSA-005"],"NOT_RUN",@J237),@T3(@J362,@J363,17,@J364,false,[@J315,"HSBI_ReserveCatchUpDigest",@J316,"HSBI_UlongToString"],[],"NOT_RUN",@J237),@T3(@J365,"HSBI_RuntimeReject",4,@J364,false,[],[],"NOT_RUN",@J237),@T3(@J365,"HSBI_RuntimePositionMatches",5,@J364,false,[],[],"NOT_RUN",@J237),@T3(@J365,@J366,6,@J364,false,[@J351,@J252,@J363,"HSBI_RuntimePositionMatches","HSBI_RuntimeReject",@J286,@J305,@J311,@J312],[],"NOT_RUN",@J237),@T3(@J367,@J368,5,@J364,false,[@J315,@J316,"HSBI_RuntimeReject",@J327,@J366],[],"NOT_RUN",@J237),@T3(@J369,@J370,5,@J364,false,["HSBI_RuntimeReject",@J366],[],"NOT_RUN",@J237)],"ModuleReview":[@T4(@J234,"71e511c620df5de7f1f9e0d865664efeaf4cf6edbcbb07f20efaf25c40e9bd62",44,"OnInit / OnDeinit / OnTick / OnTimer",@J371,@J372,@J235,[{"Name":"OnInit","Line":19,"EndLine":27},{"Name":"OnDeinit","Line":29,"EndLine":33},{"Name":"OnTick","Line":35,"EndLine":39},{"Name":"OnTimer","Line":41,"EndLine":44}],[@J373,"Include/Core/HSBI_Enums.mqh","Include/Core/HSBI_Types.mqh",@J248,@J251,@J250,@J239,@J242,@J276,@J262,@J260],["terminal timer registration"],"ENTRY_REACHABLE_FUNCTIONS",["OnInit","OnDeinit","OnTick","OnTimer"],false,"No native verification","NOT_RUN",["FSA-014"],"STATICALLY_INSPECTED",@J374),@T4(@J239,"7ae314b8f7e4183419943297885a6291afbf449a5d63490ca35757f737eb80ef",60,"HSBI_InitializeContext / HSBI_ResetContext / HSBI_ContextPositionValid / HSBI_ContextRolesConflict / HSBI_ContextPositionInScope / HSBI_ValidateContext",@J371,@J372,@J24,[{"Name":"HSBI_InitializeContext","Line":8,"EndLine":8},{"Name":"HSBI_ResetContext","Line":9,"EndLine":9},{"Name":"HSBI_ContextPositionValid","Line":10,"EndLine":18},{"Name":"HSBI_ContextRolesConflict","Line":19,"EndLine":26},{"Name":"HSBI_ContextPositionInScope","Line":27,"EndLine":32},{"Name":"HSBI_ValidateContext","Line":33,"EndLine":59}],[@J241,"Include/Core/HSBI_Roles.mqh",@J250,@J248],[],"ENTRY_REACHABLE_FUNCTIONS",["HSBI_InitializeContext"],true,"No native verification","NOT_RUN",["FSA-009"],"STATICALLY_INSPECTED",@J374),@T4("Include/Core/HSBI_Enums.mqh","69b0ded8187af3f69a4058188c206f11b881e4f7d9c092d7bafe1bb9111d29f6",11,"types/enums/contracts only",@J371,@J372,@J24,[],[],[],"INCLUDED_NOT_ENTRY_CALLED",[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J241,"a6421afab5dc291df0d17cfa4e1d39f5cc96bd87aa9cd9602129e240d0a8dd9e",24,"HSBI_IsValidIdentity / HSBI_SameCycle / HSBI_SamePositionOwner / HSBI_SameSymbolScope / HSBI_UlongToString / HSBI_SerializeIdentity",@J371,@J372,@J24,[{"Name":"HSBI_IsValidIdentity","Line":6,"EndLine":6},{"Name":"HSBI_SameCycle","Line":7,"EndLine":7},{"Name":"HSBI_SamePositionOwner","Line":8,"EndLine":8},{"Name":"HSBI_SameSymbolScope","Line":9,"EndLine":9},{"Name":"HSBI_UlongToString","Line":10,"EndLine":22},{"Name":"HSBI_SerializeIdentity","Line":23,"EndLine":23}],@J375,[],"INCLUDED_NOT_ENTRY_CALLED",[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J242,"4c4a742a62a60361fb63e907888f4bc936591c00326ebe2812ba2fa668133981",14,"HSBI_ExactlyOneFarOrZero / HSBI_NoDualTail / HSBI_NoUnknownRole / HSBI_ContextIdentityComplete / HSBI_StateRevisionMonotonic / HSBI_NoPendingActionConflict / HSBI_NoFinalReserveForPartialFar / HSBI_AllocationConservation / HSBI_RealTradingForbiddenAtHSB1",@J371,@J372,@J24,[{"Name":"HSBI_ExactlyOneFarOrZero","Line":5,"EndLine":5},{"Name":"HSBI_NoDualTail","Line":6,"EndLine":6},{"Name":"HSBI_NoUnknownRole","Line":7,"EndLine":7},{"Name":@J244,"Line":8,"EndLine":8},{"Name":"HSBI_StateRevisionMonotonic","Line":9,"EndLine":9},{"Name":@J245,"Line":10,"EndLine":10},{"Name":@J246,"Line":11,"EndLine":11},{"Name":"HSBI_AllocationConservation","Line":12,"EndLine":12},{"Name":@J247,"Line":13,"EndLine":13}],[@J239,@J259],[],"INCLUDED_NOT_ENTRY_CALLED",[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J248,"62aef3906bc933cee98a136fd8ed983be36f23ef01da50a6c2572551bce2abe2",5,"HSBI_ReasonToString",@J371,@J372,@J24,[{"Name":"HSBI_ReasonToString","Line":4,"EndLine":4}],[],[],"ENTRY_REACHABLE_FUNCTIONS",["HSBI_ReasonToString"],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4("Include/Core/HSBI_Roles.mqh","836970966be820261b031717bab2f81482ab76c57e06ee63269c368012a3399d",11,"HSBI_IsKnownRole / HSBI_ValidatePositionDescriptor / HSBI_CanPromoteToFar / HSBI_ValidateRoleTransition / HSBI_CountFarRoles",@J371,@J372,@J24,[{"Name":"HSBI_IsKnownRole","Line":6,"EndLine":6},{"Name":@J249,"Line":7,"EndLine":7},{"Name":"HSBI_CanPromoteToFar","Line":8,"EndLine":8},{"Name":"HSBI_ValidateRoleTransition","Line":9,"EndLine":9},{"Name":"HSBI_CountFarRoles","Line":10,"EndLine":10}],[@J241,"Include/Core/HSBI_Types.mqh"],[],"ENTRY_REACHABLE_FUNCTIONS",["HSBI_CountFarRoles"],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J250,"f47526eddac1c7007ebddfd5c32d95848600ba6751086442e8032ed6ce9878f2",7,@J240,@J371,@J372,@J24,[{"Name":@J240,"Line":5,"EndLine":6}],[@J251],[],"INCLUDED_NOT_ENTRY_CALLED",[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J251,"1fa087dda8d81f182c8c6d8fd2dab4c4712b973c8f95ad15c0bfdf115b01d337",30,"HSBI_BuildRuntimePolicy / HSBI_IsInjectedProofAllowed / HSBI_IsProductionPreflightAllowed / HSBI_IsBrokerDispatchAllowed / HSBI_IsStaticCalculationAllowed / HSBI_IsCompletionSourceAllowed",@J371,@J372,@J24,[{"Name":"HSBI_BuildRuntimePolicy","Line":12,"EndLine":22},{"Name":"HSBI_IsInjectedProofAllowed","Line":23,"EndLine":23},{"Name":@J252,"Line":24,"EndLine":24},{"Name":@J236,"Line":25,"EndLine":25},{"Name":@J253,"Line":26,"EndLine":26},{"Name":@J254,"Line":28,"EndLine":29}],@J376,[],"ENTRY_REACHABLE_FUNCTIONS",["HSBI_BuildRuntimePolicy",@J236],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J255,"7ec9f9860ce9d72c7f7c119377c1b2bedda25001921b92ef3aa9c7d95a32e403",11,"HSBI_IsTransitionAllowed / HSBI_ProposeStateTransition / HSBI_ApplyPureStateTransition / HSBI_ConflictTargetState / HSBI_CriticalErrorTargetState / HSBI_TransactionConflictTargetState",@J371,@J372,@J24,[{"Name":"HSBI_IsTransitionAllowed","Line":5,"EndLine":5},{"Name":"HSBI_ProposeStateTransition","Line":6,"EndLine":6},{"Name":@J256,"Line":7,"EndLine":7},{"Name":"HSBI_ConflictTargetState","Line":8,"EndLine":8},{"Name":@J257,"Line":9,"EndLine":9},{"Name":@J258,"Line":10,"EndLine":10}],@J377,["explicit Context state/revision mutation in pure apply helper"],"INCLUDED_NOT_ENTRY_CALLED",[],true,"No native verification","NOT_RUN",["FSA-012","FSA-022"],"STATICALLY_INSPECTED",@J374),@T4(@J259,"145d73d6d69baf1ef58958237b6c375bef23e2cd9004d1f50c9fe694c24077f6",6,"HSBI_ValidateStateTopology / HSBI_OutcomeCompletesAction",@J371,@J372,@J24,[{"Name":"HSBI_ValidateStateTopology","Line":4,"EndLine":4},{"Name":"HSBI_OutcomeCompletesAction","Line":5,"EndLine":5}],[@J255],[],"INCLUDED_NOT_ENTRY_CALLED",[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4("Include/Core/HSBI_Types.mqh","61e08fbfc9e97df1931ae6c825a5ff64e25f1fd4502f90e71f8b2a4c2857c3cc",8,"HSBI_Result",@J371,@J372,@J24,[{"Name":"HSBI_Result","Line":7,"EndLine":7}],@J376,[],"INCLUDED_NOT_ENTRY_CALLED",[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J373,"b9432e5d966e99a8383ea9d6308e48c62725e431dd80e4a070020e9aa63359a9",12,"types/enums/contracts only",@J371,@J372,@J24,[],[],[],"INCLUDED_NOT_ENTRY_CALLED",[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J260,"ca3590969d6b9392a5c69dc3b95878c439d316505a7e08647523a5d69e425c46",7,"HSBI_BuildDiagnosticSnapshot / HSBI_UpdateDiagnosticSnapshot",@J371,@J372,@J235,[{"Name":@J261,"Line":5,"EndLine":5},{"Name":@J238,"Line":6,"EndLine":6}],@J377,["diagnostic Print","read server timestamp for diagnostics"],"ENTRY_REACHABLE_FUNCTIONS",[@J261,@J238],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J262,"dc56e40d37909411f11dba454ec893e66315c92c68c85c1b4a9e3234daddc388",7,"HSBI_Log",@J371,@J372,@J235,[{"Name":"HSBI_Log","Line":6,"EndLine":6}],@J377,["diagnostic Print"],"ENTRY_REACHABLE_FUNCTIONS",["HSBI_Log"],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J263,"ba0d4470c5ba0dd0f39ab6fe47e026efac4808fc74a7c2e2bc0e658726ee560c",6,"HSBI_BuildPanelModel",@J371,@J372,@J235,[{"Name":"HSBI_BuildPanelModel","Line":5,"EndLine":5}],[@J260],[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J264,"f8c4c8238052aa2999b797de7cee3e39c39435bf7e42068b4d6d76994d505f01",8,"HSBI_ValidateActionRecord / HSBI_SerializeActionIds",@J371,@J372,@J33,[{"Name":"HSBI_ValidateActionRecord","Line":6,"EndLine":6},{"Name":"HSBI_SerializeActionIds","Line":7,"EndLine":7}],@J379,[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J265,"d588c6721e7a5af9e48bad54bdbe3cf3fc90688956353c3a04380ae0181f7c13",8,"HSBI_ValidateEventRecord / HSBI_SerializeEventIds",@J371,@J372,@J33,[{"Name":"HSBI_ValidateEventRecord","Line":6,"EndLine":6},{"Name":"HSBI_SerializeEventIds","Line":7,"EndLine":7}],@J379,[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J266,"67d9381fd0f2d170efc22a07bf4b391c9e86b1685d697d1e6201b713adb4d4f2",45,"HSBI_ExecutionIntentDigest / HSBI_ValidateExecutionIntentDigest / HSBI_IsValidIntentStatus / HSBI_ValidateExecutionIntentStructure / HSBI_IntentIdempotencyKey / HSBI_IsSameIntentRetry / HSBI_IsIntentConflict",@J371,@J372,@J33,[{"Name":"HSBI_ExecutionIntentDigest","Line":15,"EndLine":25},{"Name":@J267,"Line":26,"EndLine":26},{"Name":"HSBI_IsValidIntentStatus","Line":27,"EndLine":27},{"Name":@J268,"Line":28,"EndLine":41},{"Name":"HSBI_IntentIdempotencyKey","Line":42,"EndLine":42},{"Name":"HSBI_IsSameIntentRetry","Line":43,"EndLine":43},{"Name":"HSBI_IsIntentConflict","Line":44,"EndLine":44}],[@J336,@J241],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J269,"7af97449654913e8488e8dccc44c3fcf2f08b79c14ec3aea5d0388604fb5c9c0",49,"HSBI_ValidateExecutionPreflight / HSBI_IsIntentLifecycleTransitionAllowed / HSBI_IntentRetryAllowed",@J371,@J372,@J33,[{"Name":@J270,"Line":17,"EndLine":34},{"Name":@J273,"Line":35,"EndLine":46},{"Name":"HSBI_IntentRetryAllowed","Line":47,"EndLine":48}],[@J266,@J251,@J339,@J317],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J274,"01eb91c904e73d2f3973c21c37e3973b2c72cb73e295621939e132b965b65c88",33,"HSBI_ExternalOutcomeDigest / HSBI_ReconcileExecutionOutcome",@J371,@J372,@J33,[{"Name":"HSBI_ExternalOutcomeDigest","Line":13,"EndLine":19},{"Name":@J275,"Line":22,"EndLine":32}],[@J269],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J276,"d3264d4a3a8a6aef1a0cc69420f6d26b6aa16f25ec19e43f46151e6cbb242084",9,"HSBI_SubmitActionStub / HSBI_OpenPositionStub / HSBI_ClosePositionStub / HSBI_PartialCloseStub",@J371,@J372,@J33,[{"Name":"HSBI_SubmitActionStub","Line":5,"EndLine":5},{"Name":"HSBI_OpenPositionStub","Line":6,"EndLine":6},{"Name":"HSBI_ClosePositionStub","Line":7,"EndLine":7},{"Name":"HSBI_PartialCloseStub","Line":8,"EndLine":8}],@J380,[],"ENTRY_REACHABLE_FUNCTIONS",["HSBI_SubmitActionStub"],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J277,"842a28c0fa460d00c443dc9ddda2a1d5314300e3adbfb155f1876457a38f4ac7",17,"HSBI_EvaluateOwnership / HSBI_TicketMatchesObservation / HSBI_IsActualBigCoreResidual",@J371,@J372,@J33,[{"Name":"HSBI_EvaluateOwnership","Line":8,"EndLine":8},{"Name":@J278,"Line":9,"EndLine":12},{"Name":@J279,"Line":13,"EndLine":16}],[@J241,"Include/Core/HSBI_Roles.mqh",@J248],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J280,"1b244dc72cd345f0f032dde14eb89227db20a7333cbc2c72afa2046c4720d8c9",24,"HSBI_IsCompletedOutcome / HSBI_IsRetryOfSameAction / HSBI_IsFreshEvent / HSBI_TransactionBarrierPassed / HSBI_RetryAllowed",@J371,@J372,@J33,[{"Name":"HSBI_IsCompletedOutcome","Line":6,"EndLine":6},{"Name":"HSBI_IsRetryOfSameAction","Line":7,"EndLine":7},{"Name":"HSBI_IsFreshEvent","Line":8,"EndLine":8},{"Name":@J281,"Line":9,"EndLine":19},{"Name":"HSBI_RetryAllowed","Line":20,"EndLine":23}],[],[],@J378,[],true,"No native verification","NOT_RUN",["FSA-006"],"STATICALLY_INSPECTED",@J374),@T4(@J282,"b539c3c52089e22c2e5cba5a95b81bdc5267b59402bf0f3662f48e80dc1b155c",11,"HSBI_AllocatedTotal / HSBI_ValidateAllocationConservation / HSBI_ClassifyAllocationDuplicate / HSBI_CanConsumeBucket / HSBI_CanConsumeAmount",@J371,@J372,@J35,[{"Name":"HSBI_AllocatedTotal","Line":6,"EndLine":6},{"Name":@J283,"Line":7,"EndLine":7},{"Name":@J284,"Line":8,"EndLine":8},{"Name":"HSBI_CanConsumeBucket","Line":9,"EndLine":9},{"Name":"HSBI_CanConsumeAmount","Line":10,"EndLine":10}],@J375,[],@J378,[],true,"No native verification","NOT_RUN",["FSA-002","FSA-007"],"STATICALLY_INSPECTED",@J374),@T4(@J285,"f92a56ef4016231d435840b360ad8310eaa227657fddaf59dec1a3fb7001f3c0",32,"HSBI_ValidateAllocationPolicy / HSBI_AllocationPolicyDigest",@J371,@J372,@J35,[{"Name":@J286,"Line":16,"EndLine":24},{"Name":"HSBI_AllocationPolicyDigest","Line":25,"EndLine":31}],[@J294,@J241],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J287,"f2038e34a8cc22d2e98cf870e479e6a3cbfe3d6edee64855ffb8784d1e5007fb",29,"HSBI_BasketLegInput / HSBI_EvaluateBasketMoney / HSBI_BasketMoneyProofDigest",@J371,@J372,@J35,[{"Name":"HSBI_BasketLegInput","Line":7,"EndLine":10},{"Name":"HSBI_EvaluateBasketMoney","Line":11,"EndLine":19},{"Name":"HSBI_BasketMoneyProofDigest","Line":20,"EndLine":28}],[@J302,@J336],[],@J378,[],true,"No native verification","NOT_RUN",["FSA-029"],"STATICALLY_INSPECTED",@J374),@T4(@J290,"6d9734df01ff3717a537e59dfea8a345443ee558585d2e08313428e652a8e345",18,@J291,@J371,@J372,@J35,[{"Name":@J291,"Line":5,"EndLine":17}],[@J294,@J332],@J382,@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J292,"66b0389135f3438acb712d8cf694db4de24f6b7e80a4b6dad1ac249e879ab068",22,"HSBI_MoneyResult / HSBI_CalculateProjectedProfit",@J371,@J372,@J35,[{"Name":"HSBI_MoneyResult","Line":5,"EndLine":5},{"Name":@J293,"Line":6,"EndLine":21}],[@J297,@J332],@J382,@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J294,"276e9ff6308b575be208f4cc23663d7a0489d9bcce8ec67a1a9472f437a092a4",20,"HSBI_IsFiniteNumber / HSBI_ValidateBrokerProperties",@J371,@J372,@J35,[{"Name":"HSBI_IsFiniteNumber","Line":10,"EndLine":10},{"Name":@J271,"Line":11,"EndLine":19}],@J383,[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J295,"1a50a1d0c4078049c6723d4db1c7ba1409dff6fca244d10a8e7f955eee21f945",28,"HSBI_EvaluateCandidateMoney",@J371,@J372,@J35,[{"Name":"HSBI_EvaluateCandidateMoney","Line":10,"EndLine":27}],@J384,[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J296,"daab1f3d7fa18de44dea6ac293b09cd33bcc3263e691b6f3f7a5fc1dcc10b83c",17,"HSBI_EvaluateCatchUp",@J371,@J372,@J35,[{"Name":"HSBI_EvaluateCatchUp","Line":4,"EndLine":16}],[@J385],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J385,"2d54a0ac9b149a89d3f35c2b72abad97820f7ef73d2b86118389db59bd4a142a",6,"types/enums/contracts only",@J371,@J372,@J35,[],@J386,[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J297,"4f19ebab853118d7946f99a5fed2b9d84cbfd16c83390df9f5721c53c207f590",20,"HSBI_ValidateCostSnapshot / HSBI_TryActualDealNet / HSBI_TryProjectedNetMoney",@J371,@J372,@J35,[{"Name":"HSBI_ValidateCostSnapshot","Line":5,"EndLine":10},{"Name":"HSBI_TryActualDealNet","Line":11,"EndLine":14},{"Name":"HSBI_TryProjectedNetMoney","Line":15,"EndLine":19}],@J386,[],@J378,[],true,"No native verification","NOT_RUN",["FSA-019"],"STATICALLY_INSPECTED",@J374),@T4(@J299,"d9bcbef0fa7b6c5da61e7bafa6a6314458601252a2e580aac21396daadf95ed4",13,"HSBI_BuildSourceDealKey / HSBI_ValidateEconomicRecord / HSBI_SameEconomicRecord / HSBI_ClassifyEconomicDuplicate / HSBI_SerializeEconomicRecord / HSBI_IsHarvestSourceEntry",@J371,@J372,@J35,[{"Name":"HSBI_BuildSourceDealKey","Line":7,"EndLine":7},{"Name":"HSBI_ValidateEconomicRecord","Line":8,"EndLine":8},{"Name":"HSBI_SameEconomicRecord","Line":9,"EndLine":9},{"Name":@J300,"Line":10,"EndLine":10},{"Name":@J301,"Line":11,"EndLine":11},{"Name":"HSBI_IsHarvestSourceEntry","Line":12,"EndLine":12}],["Include/Core/HSBI_Enums.mqh",@J241,@J248],[],@J378,[],true,"No native verification","NOT_RUN",["FSA-001"],"STATICALLY_INSPECTED",@J374),@T4(@J302,"11e0a67346fb7ca7334d59507c44daee2c0517acee9786a251d03752f8dc774f",13,@J288,@J371,@J372,@J35,[{"Name":@J288,"Line":5,"EndLine":12}],[@J303,@J290],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J303,"cbe8d9c662250eaad105987f1540c00e56932cf9546c1bff29ca000e604a19b6",16,@J289,@J371,@J372,@J35,[{"Name":@J289,"Line":7,"EndLine":15}],[@J292,@J304],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J304,"f36029a3f62cf3d245962ea18d408555d507851e9a5e9e1e9d11c5868a28f17d",30,"HSBI_ValidateMoneyProofIdentity / HSBI_IsSameMoneyProofIdentity / HSBI_MoneyProofIdentityDigest",@J371,@J372,@J35,[{"Name":@J305,"Line":10,"EndLine":15},{"Name":@J306,"Line":16,"EndLine":22},{"Name":@J307,"Line":23,"EndLine":29}],[@J241],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J308,"0faeebfc6781198ead86e8cffac7e154947f1830e6b38d27d7900d069ac38396",6,"HSBI_ValidateMoneyState",@J371,@J372,@J35,[{"Name":"HSBI_ValidateMoneyState","Line":5,"EndLine":5}],[@J309],[],@J378,[],true,"No native verification","NOT_RUN",["FSA-008"],"STATICALLY_INSPECTED",@J374),@T4(@J309,"d7d00aa5a139ec82730e84ab18748ba49f12a339d0716255517b3377a4f94d70",10,"HSBI_BuildRecoveryPL",@J371,@J372,@J35,[{"Name":"HSBI_BuildRecoveryPL","Line":9,"EndLine":9}],[],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J310,"18a3318d954d2f2426ec715441fc159fca364cdb1b65011b449e94d0671dd00f",35,"HSBI_ValidateReserveAllocationSource / HSBI_ValidateReserveConsumption / HSBI_IsDuplicateReserveConsumption / HSBI_ReserveConsumptionConflict / HSBI_ReserveAllocationSourceDigest / HSBI_ReserveConsumptionKeyDigest",@J371,@J372,@J35,[{"Name":@J311,"Line":15,"EndLine":24},{"Name":@J312,"Line":25,"EndLine":26},{"Name":@J313,"Line":27,"EndLine":28},{"Name":@J314,"Line":29,"EndLine":30},{"Name":@J315,"Line":31,"EndLine":32},{"Name":@J316,"Line":33,"EndLine":34}],[@J285],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J317,"5d967cf22e7d0fdc3d37aae6077b15c4330526dcef4c5b8eda74340a64ff174d",83,"HSBI_ValidateReserveSourceProof / HSBI_ValidateFarLossProof / HSBI_EvaluateReserveCatchUp / HSBI_ReserveCatchUpDigest",@J371,@J372,@J35,[{"Name":@J318,"Line":24,"EndLine":29},{"Name":"HSBI_ValidateFarLossProof","Line":30,"EndLine":34},{"Name":"HSBI_EvaluateReserveCatchUp","Line":35,"EndLine":77},{"Name":"HSBI_ReserveCatchUpDigest","Line":78,"EndLine":82}],[@J310,@J303,@J251],[],@J378,[],true,"No native verification","NOT_RUN",["FSA-003","FSA-004"],"STATICALLY_INSPECTED",@J374),@T4(@J320,"aeba6d8813c0079ae4f8e5c7484895e891e6acb91ae7aeacec751977adf1f76f",45,"HSBI_ExecutionJournalEntryDigest / HSBI_ValidateJournalEntry / HSBI_IsDuplicateJournalEntry / HSBI_IsJournalEntryConflict / HSBI_ClassifyJournalAppend / HSBI_ValidateJournalChain",@J371,@J372,@J322,[{"Name":@J321,"Line":12,"EndLine":17},{"Name":"HSBI_ValidateJournalEntry","Line":18,"EndLine":20},{"Name":@J323,"Line":21,"EndLine":22},{"Name":"HSBI_IsJournalEntryConflict","Line":23,"EndLine":24},{"Name":"HSBI_ClassifyJournalAppend","Line":25,"EndLine":30},{"Name":"HSBI_ValidateJournalChain","Line":31,"EndLine":44}],[@J266],[],@J378,[],true,"ValidateJournalChain omitted from C++ adaptation","NOT_RUN",["FSA-027"],"STATICALLY_INSPECTED",@J374),@T4(@J324,"e228f6b8e2e2d0bc2aeaa8cbab6c7656412465a9f887fa8fe6b152d463e3d971",44,"HSBI_ExecutionStateSnapshotDigest / HSBI_ValidateNestedExecutionIntent / HSBI_IsActiveIntentStatus / HSBI_ValidateExecutionStateSnapshot / HSBI_RecoverExecutionState",@J371,@J372,@J322,[{"Name":@J325,"Line":12,"EndLine":18},{"Name":@J326,"Line":19,"EndLine":24},{"Name":"HSBI_IsActiveIntentStatus","Line":25,"EndLine":26},{"Name":@J327,"Line":27,"EndLine":41},{"Name":"HSBI_RecoverExecutionState","Line":42,"EndLine":43}],[@J320],[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J328,"800b8610c306a6d197df37b99ad93da09278f09a68049543578577d2348d80c8",8,"HSBI_ValidateJournalRecord / HSBI_SerializeJournalIds",@J371,@J372,@J322,[{"Name":"HSBI_ValidateJournalRecord","Line":6,"EndLine":6},{"Name":"HSBI_SerializeJournalIds","Line":7,"EndLine":7}],[@J264,@J265],[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J329,"e72b591500db88e2596c498fcdf7dbfdbe3641eef91ebbee80ce59e3aeddab06",8,"HSBI_PersistSnapshotStub",@J371,@J372,@J322,[{"Name":"HSBI_PersistSnapshotStub","Line":7,"EndLine":7}],[@J331,@J328],[],@J378,[],false,"No native verification","NOT_RUN",["FSA-013"],"STATICALLY_INSPECTED",@J374),@T4(@J330,"dc7260cd56d8392664ebecfb9fd3790cfe768f1a1ab9d428ed6bf83c14679c0d",8,"HSBI_CompareReconciliation",@J371,@J372,@J322,[{"Name":"HSBI_CompareReconciliation","Line":7,"EndLine":7}],[@J331],[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J331,"d40945509150276d1e8ca60de173cf64af3a6ddff91f5ac1361c8533d41a5b9e",11,"HSBI_ValidateSnapshotSchema / HSBI_TestDigest / HSBI_SerializeSnapshotIds",@J371,@J372,@J322,[{"Name":"HSBI_ValidateSnapshotSchema","Line":8,"EndLine":8},{"Name":"HSBI_TestDigest","Line":9,"EndLine":9},{"Name":"HSBI_SerializeSnapshotIds","Line":10,"EndLine":10}],[@J239,@J334,@J264,@J308],[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J332,"4cb955469a6c502456d9db146cb5fd80568807cc23abcdcdd9bcf5e4f4dd110c",38,"HSBI_GridTolerance / HSBI_IsPriceOnTickGrid / HSBI_NormalizePriceToTick / HSBI_ValidatePriceGrid / HSBI_PriceDistanceInTicks / HSBI_IsVolumeOnGrid / HSBI_FloorVolumeToStep / HSBI_CeilVolumeToStep / HSBI_NormalizeVolume / HSBI_ValidateVolume",@J371,@J372,@J30,[{"Name":"HSBI_GridTolerance","Line":7,"EndLine":7},{"Name":"HSBI_IsPriceOnTickGrid","Line":8,"EndLine":12},{"Name":"HSBI_NormalizePriceToTick","Line":13,"EndLine":18},{"Name":"HSBI_ValidatePriceGrid","Line":19,"EndLine":19},{"Name":"HSBI_PriceDistanceInTicks","Line":20,"EndLine":20},{"Name":"HSBI_IsVolumeOnGrid","Line":21,"EndLine":25},{"Name":"HSBI_FloorVolumeToStep","Line":26,"EndLine":26},{"Name":"HSBI_CeilVolumeToStep","Line":27,"EndLine":27},{"Name":"HSBI_NormalizeVolume","Line":28,"EndLine":32},{"Name":"HSBI_ValidateVolume","Line":33,"EndLine":37}],@J386,[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J334,"3643a4a741e24e293656674b3681a74a5ef448610428f28a07dbf355533ac856",9,"HSBI_ValidateCandidatePlan / HSBI_CandidatePlanFingerprint / HSBI_SameCandidatePlan",@J371,@J372,@J30,[{"Name":"HSBI_ValidateCandidatePlan","Line":6,"EndLine":6},{"Name":@J335,"Line":7,"EndLine":7},{"Name":"HSBI_SameCandidatePlan","Line":8,"EndLine":8}],[@J387,@J241],[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J336,"5bd35f0cc4b7ee1aac1a772b2932f13ba385922e26d5f2649bbda76837256a4b",25,"HSBI_IsSnapshotFresh / HSBI_NormalizePriceToTick / HSBI_ResolveCloseSide / HSBI_ValidateMarketSnapshot / HSBI_ValidateControlPriceSet / HSBI_ValidateTypedControlPrice",@J371,@J372,@J30,[{"Name":"HSBI_IsSnapshotFresh","Line":11,"EndLine":11},{"Name":"HSBI_NormalizePriceToTick","Line":12,"EndLine":12},{"Name":"HSBI_ResolveCloseSide","Line":13,"EndLine":13},{"Name":"HSBI_ValidateMarketSnapshot","Line":14,"EndLine":14},{"Name":@J337,"Line":15,"EndLine":15},{"Name":@J272,"Line":16,"EndLine":24}],["Include/Core/HSBI_Types.mqh",@J248,@J332],[],@J378,[],true,"No native verification","NOT_RUN",["FSA-021"],"STATICALLY_INSPECTED",@J374),@T4("Include/Planning/HSBI_DecisionResult.mqh","cb5f7cd0c719ca81ad35547d49af8ba827d94d3bb41dbb88c0451eebf306849d",5,"types/enums/contracts only",@J371,@J372,@J30,[],@J380,[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J339,"7bea2c75eec23825d5cbcca82fa72022b73f8c1626f5ffbce30ac79d722b03a0",60,"HSBI_AggregateDigest / HSBI_AggregateFutureSmallProof",@J371,@J372,@J30,[{"Name":"HSBI_AggregateDigest","Line":16,"EndLine":22},{"Name":@J340,"Line":23,"EndLine":59}],@J384,[],@J378,[],true,"No native verification","NOT_RUN",["FSA-015"],"STATICALLY_INSPECTED",@J374),@T4(@J341,"c403bbad6089076500823219dac296e69100bed0e2cb950eb1f248749b868cf6",151,"HSBI_CalculateFutureSmallDepth / HSBI_ValidateConservativeBound / HSBI_ValidateLevelMarket / HSBI_ValidateLevelCosts / HSBI_ValidateFarProjection / HSBI_LevelControlPrice / HSBI_ValidateFutureSmallInput / HSBI_EvaluateFutureSmallLevel / HSBI_FutureSmallLevelDigest / HSBI_FutureSmallProofDigest / HSBI_SolveFutureSmall",@J371,@J372,@J30,[{"Name":@J342,"Line":5,"EndLine":11},{"Name":@J343,"Line":12,"EndLine":17},{"Name":"HSBI_ValidateLevelMarket","Line":18,"EndLine":26},{"Name":"HSBI_ValidateLevelCosts","Line":27,"EndLine":31},{"Name":"HSBI_ValidateFarProjection","Line":32,"EndLine":38},{"Name":"HSBI_LevelControlPrice","Line":39,"EndLine":44},{"Name":@J344,"Line":45,"EndLine":56},{"Name":@J345,"Line":57,"EndLine":92},{"Name":"HSBI_FutureSmallLevelDigest","Line":93,"EndLine":105},{"Name":"HSBI_FutureSmallProofDigest","Line":106,"EndLine":112},{"Name":"HSBI_SolveFutureSmall","Line":113,"EndLine":150}],[@J388,@J251],[],@J378,[],true,"No native verification","NOT_RUN",["FSA-017","FSA-018","FSA-028"],"STATICALLY_INSPECTED",@J374),@T4(@J388,"16fcecb00c05f2e03b90f81823bdf1c2aac4a7b6263713b29ad9feb18b218325",82,"types/enums/contracts only",@J371,@J372,@J30,[],[@J347,@J287,@J285,@J359],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J347,"62b3b4a8d7a374e15b96b46a380e3c2f8f0e74aa57ae8749c0261ebab27a11f9",38,"HSBI_ValidateRecoverySlope / HSBI_EvaluateRecoveryMoneyDirection / HSBI_SolveBigGeometry",@J371,@J372,@J30,[{"Name":"HSBI_ValidateRecoverySlope","Line":6,"EndLine":11},{"Name":@J348,"Line":12,"EndLine":20},{"Name":"HSBI_SolveBigGeometry","Line":21,"EndLine":37}],[@J387,@J332],[],@J378,[],true,"No native verification","NOT_RUN",["FSA-011"],"STATICALLY_INSPECTED",@J374),@T4(@J387,"3126ecc200269b885bf2b5b46b8e72356f61e176b829ab0f40ee307e5b4e8b49",7,"types/enums/contracts only",@J371,@J372,@J30,[],[@J336],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J349,"9e09da3a5d22579807375be836931a11ecf666e79108dde2c9724f60f1cd2bf1",42,"HSBI_ValidateNewFarCandidateStructure / HSBI_IsCandidateSourceValid / HSBI_IsCompleteCandidateProof / HSBI_CompareCandidateTieBreak",@J371,@J372,@J30,[{"Name":@J350,"Line":19,"EndLine":23},{"Name":"HSBI_IsCandidateSourceValid","Line":24,"EndLine":25},{"Name":@J351,"Line":26,"EndLine":32},{"Name":@J352,"Line":33,"EndLine":41}],@J383,[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J353,"9dcf60b6edc245a8a5ee3a05f35d4d8d26c12479f570a66aa5e4f0e703497cd2",154,"HSBI_FutureSmallTemplateDigest / HSBI_NewFarInputDigest / HSBI_FinalizeNewFarPlanDigest / HSBI_ValidateNewFarSource / HSBI_AllowedTransitionLoss / HSBI_BuildCandidateFutureSmallInput / HSBI_NewFarProofIdentity / HSBI_CandidateProofDigest / HSBI_SolveNewFar",@J371,@J372,@J30,[{"Name":@J354,"Line":35,"EndLine":46},{"Name":"HSBI_NewFarInputDigest","Line":47,"EndLine":58},{"Name":@J355,"Line":59,"EndLine":59},{"Name":"HSBI_ValidateNewFarSource","Line":60,"EndLine":73},{"Name":"HSBI_AllowedTransitionLoss","Line":74,"EndLine":74},{"Name":@J356,"Line":75,"EndLine":79},{"Name":"HSBI_NewFarProofIdentity","Line":80,"EndLine":83},{"Name":"HSBI_CandidateProofDigest","Line":84,"EndLine":93},{"Name":"HSBI_SolveNewFar","Line":94,"EndLine":153}],[@J349,@J339,@J277,@J360,@J295,@J317],[],@J378,[],false,"No native verification","NOT_RUN",["FSA-010","FSA-023"],"STATICALLY_INSPECTED",@J374),@T4(@J357,"64791ac97362dfd8a5bcf5e5b294b1b71f8d984acc10a41853d27e20328e0900",14,"HSBI_FailClosed / HSBI_CalculationResultFlagsValid",@J371,@J372,@J44,[{"Name":"HSBI_FailClosed","Line":6,"EndLine":9},{"Name":@J358,"Line":10,"EndLine":13}],@J386,[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J359,"8ffa044f6819186aac145df165c80a32c0d7225142b28d3ef413326518277f7b",52,@J346,@J371,@J372,@J44,[{"Name":@J346,"Line":29,"EndLine":51}],[@J287],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J360,"d82738006b15bb85990171b96cf65662a2699b6b890501fdd6cf31e73c1e9272",18,"HSBI_EvaluateNewFarGates",@J371,@J372,@J44,[{"Name":"HSBI_EvaluateNewFarGates","Line":6,"EndLine":17}],[@J357],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J361,"d0d7072973dac81be9284562046b7227ecfafbe14962c9ad05a3f8e2c73585c8",7,"HSBI_ValidateRiskInput",@J371,@J372,@J44,[{"Name":"HSBI_ValidateRiskInput","Line":6,"EndLine":6}],[@J389,@J248],[],@J378,[],true,"No native verification","NOT_RUN",["FSA-005"],"STATICALLY_INSPECTED",@J374),@T4(@J389,"327b2b000c136c19340ebcdca287341b7866da9bd209aac713ae393700c6bf4d",5,"types/enums/contracts only",@J371,@J372,@J44,[],[],[],@J378,[],true,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J362,"cacba88273d9d85bd34f09d978178fc89fdceb672b3651cba683aea1679110f4",18,@J363,@J371,@J372,@J364,[{"Name":@J363,"Line":17,"EndLine":17}],[@J239,@J251,@J339,@J349,@J317,@J324],[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J365,"0332a192d4b9a5389f377d252111fb0317f074bc9ff7b51658a9e8de2d5fbd9b",30,"HSBI_RuntimeReject / HSBI_RuntimePositionMatches / HSBI_ValidateRuntimeDecisionContext",@J371,@J372,@J364,[{"Name":"HSBI_RuntimeReject","Line":4,"EndLine":4},{"Name":"HSBI_RuntimePositionMatches","Line":5,"EndLine":5},{"Name":@J366,"Line":6,"EndLine":29}],[@J362],[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J367,"ec27d83911b89a77c31a6d7347a700e31e8bf631268aaaddfe4eedf976b5cbe7",18,@J368,@J371,@J372,@J364,[{"Name":@J368,"Line":5,"EndLine":17}],[@J365],[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J369,"0e04217f0bd873a784ab65cc87514c7deb65c149b8b23fa7218d885b5cf30f1a",19,@J370,@J371,@J372,@J364,[{"Name":@J370,"Line":5,"EndLine":18}],[@J367],[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4("Include/Scenarios/HSBI_BigHarvestTypes.mqh","0516b1ec1b5720265df3072d28035719d3ed369f29c8bb28177b94a98873f483",5,"types/enums/contracts only",@J371,@J372,@J390,[],@J392,[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4("Include/Scenarios/HSBI_FinalCloseTypes.mqh","3adfe776abae340a17b8ae8977c848f15c3b89cc2216085e71a9bf59ae6c53cd",5,"types/enums/contracts only",@J371,@J372,@J390,[],@J392,[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4("Include/Scenarios/HSBI_InitialLockTypes.mqh","f67baeae393cc58d4d584eb9b22819991ba281f7986f7273d1672a1def634262",5,"types/enums/contracts only",@J371,@J372,@J390,[],@J392,[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4("Include/Scenarios/HSBI_PartialFarTypes.mqh","ea862ce2f05239cc7aef8a94a256f4eaa50534c37f55d3d6c59d5ea6cf545fc5",5,"types/enums/contracts only",@J371,@J372,@J390,[],@J392,[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4(@J391,"7cc05c0455d372ef7219b3ac4b86e9b8f2753131bcd8a5ea2819bd8a90dff1f3",6,"types/enums/contracts only",@J371,@J372,@J390,[],@J375,[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374),@T4("Include/Scenarios/HSBI_SmallTransitionTypes.mqh","abf62239594b699449646178cfffaf4e15b6317eec9728088fcd98a76531cef1",5,"types/enums/contracts only",@J371,@J372,@J390,[],@J392,[],@J378,[],false,"No native verification","NOT_RUN",[],"STATICALLY_INSPECTED",@J374)],"AllowedVerdicts":["VERIFIED","PARTIALLY_VERIFIED","CONTRADICTORY","UNIMPLEMENTED","UNTESTED","UNSPECIFIED","NOT_APPLICABLE"],"AuditCompleteness":"PARTIAL"}
@T1=OBJECT_KEYS["Section","SourceFile","Line","EndLine","Assertion","Verdict","CodeOwner","Evidence","Boundary"]
@T2=OBJECT_KEYS["RequirementID","SourceFile","Line","Section","Text","CodeOwner","Status","Evidence","ReviewBoundary"]
@T3=OBJECT_KEYS["File","Function","Line","OwnerDocument","ReachableFromEA","StaticCalls","DefectIDs","NativeStatus","FunctionalEvidence"]
@T4=OBJECT_KEYS["File","SHA256","Lines","Purpose","Input","Output","OwnerDocument","Functions","Dependencies","SideEffects","EntryUse","EntryFunctions","CppBodyIncluded","AdapterLimitation","NativeEvidence","DefectIDs","ReviewStatus","NotClaimed"]
@J1="4185b84f7a6a8847f6a9c5796f07113907be447d"
@J2="Docs/03_FULL_SYSTEM_MANUAL_RU.md"
@J3="`IDLE → Initial Lock actual fills → close INITIAL_PLUS actual deal → FAR → immutable CandidatePlan → C/T/S basket actual fills → Big Harvest → Allocation → Final Close или Partial Far`, либо `Small confirmation → immutable transition → close SMALL_BASE → OldFar → BIG_TREND → planned BIG_CORE part → actual BIG_CORE residual → NEW_FAR → FAR нового цикла`."
@J4="See owner chapter/module matrix; not whole-cycle implementation"
@J5="EXTRACTED.json, REFERENCE.json, state/call matrices"
@J6="Owner specification vs actual source; PARTIAL/UNIMPLEMENTED are not native PASS"
@J7="Far SELL: BIG_CORE и BIG_TREND BUY, SMALL_BASE SELL. Far BUY: BIG_CORE и BIG_TREND SELL, SMALL_BASE BUY. BUY close рассчитывается по Bid, SELL close по Ask. Одновременно допускается только один FAR."
@J8="`C=FloorBrokerGrid(F×Rc)`, `T=FloorBrokerGrid(F×Rt)`, `S=CeilBrokerGrid(F×Rs)`, `Bnet=C+T-S`. После округления обязательны: `Bnet-F>0`; broker-money Reserve Catch-Up; `RecoveryPL(P+tick)>RecoveryPL(P)` на проверяемом диапазоне; compression `0<N<F` с risk/margin/next-cycle gates. Rc>0, Rt≥0, Rs>0; любые NaN, overflow, invalid volume или failed proof дают reject. Demonstration profile не является default."
@J9="CurrentClosePrice, NextBigControlPrice, SmallTransitionControlPrice, AdverseRiskControlPrice, GapStressPrice, FinalClosePrice всегда содержат Bid/Ask side, tick-normalized price, timestamp и freshness. Stale snapshot блокирует действие."
@J10="CandidatePlan и Future Small"
@J11="Plan immutable и связан с Account+Symbol+Magic+CycleID+StateRevision+market snapshot. Future Small проверяется exact recursion до terminal/depth/bound, затем conservative `F(k+j)≤q^jF(k)`, 0<q<1. Depth 1 не является доказательством."
@J12="Solver перебирает broker-valid N по возрастанию и выбирает minimum-safe. Fixed TargetNewFarRatio не является solver. Tie-break: RiskNext, MarginNext, expected transitions, safety buffer, N. Источник NEW_FAR — только actual remaining original BIG_CORE ticket/identifier после подтверждённых fills."
@J13="`DealNet=Profit+Swap+Commission+Fee`. Initial Profit и opening DEAL_ENTRY_IN исключены. Для каждого SourceDealKey: `FinalReserve+PartialFar+Transition+Carry+Residual=AllocatableDealNet`; отрицательный DealNet не распределяется как прибыль. EventKey и ConsumptionKey обеспечивают exactly-once. FinalReserve никогда не используется Partial Far."
@J14="Только PartialFarBudget резервируется; `CloseLotRaw=Budget/FarCloseLossPerLot`, затем floor по broker step и повторная проверка стоимости. Actual consumption определяется actual closing DealNet. Unused reservation освобождается. Partial fill блокирует следующий шаг."
@J15="`TransitionNet=ΣActualClosingDealNet`, `TransitionLoss=max(0,-TransitionNet)`. Разрешённый loss — минимум absolute cap, equity cap, OldFar-risk cap и cumulative-cycle cap."
@J16="Единая authority: `RecoveryPLCloseNow ≥ MinimumRecoveryProfitMoney + ExecutionSafetyBufferMoney + MoneyTolerance`, где `RecoveryPLCloseNow=RealizedCycleNet+ΣOpenPositionCloseNowNet`. Allocation buckets повторно не прибавляются. Дополнительно обязательны reconciled positions, no pending actions, no unknown deals, valid ownership, fresh FinalClosePrice, costs and allowed coverage."
@J17="Touch недостаточен. Нужны close-side touch, повторный fresh snapshot, configurable hold/retrace, persisted debounce key и отсутствие active transition. Duplicate trigger — NO-OP."
@J18="Transaction, retry и timeout"
@J19="`Plan→Action→Persist→Request→OnTradeTransaction→fill accumulation→actual state→ledger→persist→FSM advance`. REQUEST_SENT/PLACED/DONE_PARTIAL не равны completed. Retry допускается только с тем же ActionID, после history check, при отсутствии completed deal, reconciliation=PENDING и исключённом duplicate request. TIMEOUT не равен failure или completed и ведёт в reconciliation."
@J20="Перед открытием: ownership→freshness→spread→volume→margin→free margin→drawdown→gross exposure→worst case. Неизвестное значение = fail-closed. Emergency Liquidation отделена от recovery Final Close, не получает recovery PASS, блокирует открытия и требует manual review/no auto-resume."
@J21="Scope, persistence и REAL_LIMITED"
@J22="Identity: AccountLogin+Symbol+Magic+CycleID+PositionIdentifier+Role. Generation 1: один цикл на Symbol+Magic; multi-symbol только при полной изоляции. Persistence: crash-consistent versioned file commit protocol, canonical serialization, SHA-256, temp write, reread verify, commit marker, previous snapshot, append-only journal, per-identity lock. REAL_LIMITED запрещён до всех readiness gates, Demo Forward PASS и отдельного одобрения администратора."
@J23="Docs/00_PROJECT_CHARTER_RU.md"
@J24="Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md; Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md"
@J25="Scoped functions/formulas/cases, not all assertions in this row are proved"
@J26="Preconditions / Postconditions"
@J27="Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md"
@J28="Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md"
@J29="Docs/04_MATHEMATICAL_MODEL_RU.md"
@J30="Docs/04_MATHEMATICAL_MODEL_RU.md; Docs/05_GEOMETRY_MODEL_RU.md; Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md"
@J31="Docs/05_GEOMETRY_MODEL_RU.md"
@J32="Docs/06_STATE_MACHINE_SPECIFICATION_RU.md"
@J33="Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md"
@J34="Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md"
@J35="Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md"
@J36="Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md"
@J37="Docs/10_BIG_HARVEST_SPECIFICATION_RU.md"
@J38="10. Полная спецификация Big Harvest"
@J39="Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md"
@J40="Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md"
@J41="12. Единый нормативный Final Close"
@J42="Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md"
@J43="Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md"
@J44="Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md"
@J45="Docs/16_PERSISTENCE_AND_RESTART_RU.md"
@J46="Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md"
@J47="17. Reconciliation и terminal-safe recovery routes"
@J48="Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md"
@J49="Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md"
@J51="INDEXED historical traceability/status table; not semantic acceptance of every row"
@J64="19. Матрица требований и MQL5 mapping HSB.1"
@J70="Нормативный статус HSB.1V (2026-08-10)"
@J76="Единый итоговый статус HSB.1V (2026-08-11)"
@J79="HSB.2B — Future Small и NewFar Solver"
@J80="HSB.2B-R — корректировка broker-money proof"
@J82="HSB.2B-R2 — allocation, level snapshots и proof isolation"
@J83="HSB.2B-R3 — multi-level aggregation и allocation consumption"
@J199="Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md"
@J200="Критерии production-готовности"
@J201="Docs/22_OPEN_DECISIONS_REGISTER_RU.md"
@J202="Hybrid Split Big Independent EA"
@J203="Docs/23_NORMATIVE_DECISIONS_RESOLUTION_RU.md"
@J204="23. Полный нормативный реестр решений Hybrid Split Big"
@J205="Docs/24_BROKER_MONEY_MODEL_RU.md"
@J206="24. Broker-Money Model HSB.2A"
@J212="Docs/25_BROKER_GRID_AND_ROUNDING_RU.md"
@J213="25. Broker Grid и rounding HSB.2A"
@J214="Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md"
@J215="Docs/27_CONTROL_PRICES_AND_COSTS_RU.md"
@J216="27. Control Prices и Costs HSB.2A"
@J217="Docs/27_FUTURE_SMALL_SOLVER_RU.md"
@J218="27. Future Small Solver HSB.2B"
@J225="Docs/28_NEW_FAR_SOLVER_RU.md"
@J226="Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md"
@J227="29. Candidate objective и tie-break HSB.2B"
@J228="Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md"
@J229="30. Aggregate proof Future Small"
@J230="Docs/31_MONEY_PROOF_IDENTITY_RU.md"
@J231="31. Identity broker-money proof"
@J232="Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md"
@J233="32. Reserve allocation и consumption"
@J234="Hybrid_Split_Big_Independent_EA.mq5"
@J235="Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md; Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md"
@J236="HSBI_IsBrokerDispatchAllowed"
@J237="Specific EXTRACTED cases only; compilation of helper definitions not execution of every function"
@J238="HSBI_UpdateDiagnosticSnapshot"
@J239="Include/Core/HSBI_Context.mqh"
@J240="HSBI_IsRuntimeModeAllowedAtStage1"
@J241="Include/Core/HSBI_Identifiers.mqh"
@J242="Include/Core/HSBI_Invariants.mqh"
@J243=["HSBI_IsKnownRole","HSBI_Result"]
@J244="HSBI_ContextIdentityComplete"
@J245="HSBI_NoPendingActionConflict"
@J246="HSBI_NoFinalReserveForPartialFar"
@J247="HSBI_RealTradingForbiddenAtHSB1"
@J248="Include/Core/HSBI_ReasonCodes.mqh"
@J249="HSBI_ValidatePositionDescriptor"
@J250="Include/Core/HSBI_RuntimeMode.mqh"
@J251="Include/Core/HSBI_RuntimePolicy.mqh"
@J252="HSBI_IsProductionPreflightAllowed"
@J253="HSBI_IsStaticCalculationAllowed"
@J254="HSBI_IsCompletionSourceAllowed"
@J255="Include/Core/HSBI_StateMachine.mqh"
@J256="HSBI_ApplyPureStateTransition"
@J257="HSBI_CriticalErrorTargetState"
@J258="HSBI_TransactionConflictTargetState"
@J259="Include/Core/HSBI_StateValidator.mqh"
@J260="Include/Diagnostics/HSBI_Diagnostics.mqh"
@J261="HSBI_BuildDiagnosticSnapshot"
@J262="Include/Diagnostics/HSBI_Logger.mqh"
@J263="Include/Diagnostics/HSBI_PanelModel.mqh"
@J264="Include/Execution/HSBI_ActionTypes.mqh"
@J265="Include/Execution/HSBI_EventTypes.mqh"
@J266="Include/Execution/HSBI_ExecutionIntent.mqh"
@J267="HSBI_ValidateExecutionIntentDigest"
@J268="HSBI_ValidateExecutionIntentStructure"
@J269="Include/Execution/HSBI_ExecutionPreflight.mqh"
@J270="HSBI_ValidateExecutionPreflight"
@J271="HSBI_ValidateBrokerProperties"
@J272="HSBI_ValidateTypedControlPrice"
@J273="HSBI_IsIntentLifecycleTransitionAllowed"
@J274="Include/Execution/HSBI_ExternalOutcome.mqh"
@J275="HSBI_ReconcileExecutionOutcome"
@J276="Include/Execution/HSBI_NoTradeExecution.mqh"
@J277="Include/Execution/HSBI_OwnershipGuardTypes.mqh"
@J278="HSBI_TicketMatchesObservation"
@J279="HSBI_IsActualBigCoreResidual"
@J280="Include/Execution/HSBI_TransactionTypes.mqh"
@J281="HSBI_TransactionBarrierPassed"
@J282="Include/Money/HSBI_AllocationLedgerTypes.mqh"
@J283="HSBI_ValidateAllocationConservation"
@J284="HSBI_ClassifyAllocationDuplicate"
@J285="Include/Money/HSBI_AllocationPolicyTypes.mqh"
@J286="HSBI_ValidateAllocationPolicy"
@J287="Include/Money/HSBI_BasketMoneyEvaluator.mqh"
@J288="HSBI_EvaluateProjectedLegMargin"
@J289="HSBI_EvaluateProjectedLegMoney"
@J290="Include/Money/HSBI_BrokerMarginModel.mqh"
@J291="HSBI_CalculateProjectedMargin"
@J292="Include/Money/HSBI_BrokerMoneyModel.mqh"
@J293="HSBI_CalculateProjectedProfit"
@J294="Include/Money/HSBI_BrokerMoneyTypes.mqh"
@J295="Include/Money/HSBI_CandidateMoneyEvaluator.mqh"
@J296="Include/Money/HSBI_CatchUpModel.mqh"
@J297="Include/Money/HSBI_CostModel.mqh"
@J298=["HSBI_IsFiniteNumber","HSBI_ValidateCostSnapshot"]
@J299="Include/Money/HSBI_EconomicLedgerTypes.mqh"
@J300="HSBI_ClassifyEconomicDuplicate"
@J301="HSBI_SerializeEconomicRecord"
@J302="Include/Money/HSBI_LevelMarginEvaluator.mqh"
@J303="Include/Money/HSBI_LevelMoneyEvaluator.mqh"
@J304="Include/Money/HSBI_MoneyProofIdentity.mqh"
@J305="HSBI_ValidateMoneyProofIdentity"
@J306="HSBI_IsSameMoneyProofIdentity"
@J307="HSBI_MoneyProofIdentityDigest"
@J308="Include/Money/HSBI_MoneyState.mqh"
@J309="Include/Money/HSBI_MoneyTypes.mqh"
@J310="Include/Money/HSBI_ReserveAllocationTypes.mqh"
@J311="HSBI_ValidateReserveAllocationSource"
@J312="HSBI_ValidateReserveConsumption"
@J313="HSBI_IsDuplicateReserveConsumption"
@J314="HSBI_ReserveConsumptionConflict"
@J315="HSBI_ReserveAllocationSourceDigest"
@J316="HSBI_ReserveConsumptionKeyDigest"
@J317="Include/Money/HSBI_ReserveCatchUpEvaluator.mqh"
@J318="HSBI_ValidateReserveSourceProof"
@J319=["HSBI_IsFiniteNumber",@J306,@J305]
@J320="Include/Persistence/HSBI_ExecutionJournal.mqh"
@J321="HSBI_ExecutionJournalEntryDigest"
@J322="Docs/16_PERSISTENCE_AND_RESTART_RU.md; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md"
@J323="HSBI_IsDuplicateJournalEntry"
@J324="Include/Persistence/HSBI_ExecutionStateSnapshot.mqh"
@J325="HSBI_ExecutionStateSnapshotDigest"
@J326="HSBI_ValidateNestedExecutionIntent"
@J327="HSBI_ValidateExecutionStateSnapshot"
@J328="Include/Persistence/HSBI_JournalTypes.mqh"
@J329="Include/Persistence/HSBI_PersistenceInterface.mqh"
@J330="Include/Persistence/HSBI_ReconciliationTypes.mqh"
@J331="Include/Persistence/HSBI_SnapshotTypes.mqh"
@J332="Include/Planning/HSBI_BrokerGrid.mqh"
@J333=["HSBI_GridTolerance","HSBI_IsFiniteNumber"]
@J334="Include/Planning/HSBI_CandidatePlan.mqh"
@J335="HSBI_CandidatePlanFingerprint"
@J336="Include/Planning/HSBI_ControlPrices.mqh"
@J337="HSBI_ValidateControlPriceSet"
@J338=["HSBI_GridTolerance","HSBI_IsFiniteNumber","HSBI_IsPriceOnTickGrid"]
@J339="Include/Planning/HSBI_FutureSmallProofAggregator.mqh"
@J340="HSBI_AggregateFutureSmallProof"
@J341="Include/Planning/HSBI_FutureSmallSolver.mqh"
@J342="HSBI_CalculateFutureSmallDepth"
@J343="HSBI_ValidateConservativeBound"
@J344="HSBI_ValidateFutureSmallInput"
@J345="HSBI_EvaluateFutureSmallLevel"
@J346="HSBI_EvaluateFutureSmallRisk"
@J347="Include/Planning/HSBI_GeometrySolver.mqh"
@J348="HSBI_EvaluateRecoveryMoneyDirection"
@J349="Include/Planning/HSBI_NewFarCandidate.mqh"
@J350="HSBI_ValidateNewFarCandidateStructure"
@J351="HSBI_IsCompleteCandidateProof"
@J352="HSBI_CompareCandidateTieBreak"
@J353="Include/Planning/HSBI_NewFarSolver.mqh"
@J354="HSBI_FutureSmallTemplateDigest"
@J355="HSBI_FinalizeNewFarPlanDigest"
@J356="HSBI_BuildCandidateFutureSmallInput"
@J357="Include/Risk/HSBI_CalculationGateTypes.mqh"
@J358="HSBI_CalculationResultFlagsValid"
@J359="Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh"
@J360="Include/Risk/HSBI_NewFarGateTypes.mqh"
@J361="Include/Risk/HSBI_RiskGateResult.mqh"
@J362="Include/Runtime/HSBI_RuntimeDecisionTypes.mqh"
@J363="HSBI_RuntimeDecisionContextDigest"
@J364="Docs/HSB_2D_RUNTIME_INTEGRATION_RU.md; Docs/HSB_2D_TRANSACTION_BARRIER_RU.md"
@J365="Include/Runtime/HSBI_RuntimeDecisionValidator.mqh"
@J366="HSBI_ValidateRuntimeDecisionContext"
@J367="Include/Runtime/HSBI_RuntimeRestartValidator.mqh"
@J368="HSBI_ValidateRestartedRuntimeState"
@J369="Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh"
@J370="HSBI_CanAdvanceRuntimeDecision"
@J371="Declared source DTOs/parameters (exact signature/source in INVENTORY Functions)"
@J372="Declared return DTO/status/bool/digest; full source retained"
@J373="Include/Core/HSBI_Version.mqh"
@J374="No file-level native correctness or complete function test coverage inferred from file existence/adapter compilation"
@J375=["Include/Core/HSBI_Enums.mqh",@J248]
@J376=["Include/Core/HSBI_Enums.mqh"]
@J377=[@J239]
@J378="DORMANT_LIBRARY_NOT_INCLUDED_BY_EA"
@J379=["Include/Core/HSBI_Enums.mqh",@J241]
@J380=[@J248]
@J381="calculation-only broker API; not executed in MT5"
@J382=[@J381]
@J383=["Include/Core/HSBI_Types.mqh",@J248]
@J384=[@J341]
@J385="Include/Money/HSBI_CatchUpTypes.mqh"
@J386=[@J294]
@J387="Include/Planning/HSBI_GeometryTypes.mqh"
@J388="Include/Planning/HSBI_FutureSmallTypes.mqh"
@J389="Include/Risk/HSBI_RiskTypes.mqh"
@J390="Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md through Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md"
@J391="Include/Scenarios/HSBI_ScenarioTypes.mqh"
@J392=[@J391]
```


## AUDIT02 FSM: полная матрица без повторения постоянных полей

1089 records представлены 33 строками по33битам;1=true,0=false, порядок строк/столбцов совпадает ActualStates. Все остальные поля каждого record побайтно одинаковы и раскрыты в CONSTANTS. Проверены keys,порядок,размер каждого блока; это перекодирование статической таблицы, не вызов production predicate. Все6518символов прочитаны.

```text
ROOT={"ActualStates":["HSBI_STATE_DISABLED","HSBI_STATE_IDLE",@J1,@J2,@J3,@J4,@J5,"HSBI_STATE_FAR_ACTIVE",@J6,@J7,@J8,@J9,"HSBI_STATE_BASKET_ACTIVE",@J10,@J11,@J12,@J13,@J14,@J15,@J16,@J17,"HSBI_STATE_SMALL_CONFIRMING","HSBI_STATE_SMALL_CLOSING","HSBI_STATE_OLD_FAR_CLOSING",@J18,@J19,@J20,"HSBI_STATE_RETRY_PENDING","HSBI_STATE_RECONCILING","HSBI_STATE_EMERGENCY","HSBI_STATE_MANUAL_REVIEW","HSBI_STATE_TERMINAL_SAFE","HSBI_STATE_CYCLE_CLOSED"],"ActualPurePairs":@BOOLEAN_MATRIX(ROW_AND_COLUMN_ORDER=["HSBI_STATE_DISABLED","HSBI_STATE_IDLE",@J1,@J2,@J3,@J4,@J5,"HSBI_STATE_FAR_ACTIVE",@J6,@J7,@J8,@J9,"HSBI_STATE_BASKET_ACTIVE",@J10,@J11,@J12,@J13,@J14,@J15,@J16,@J17,"HSBI_STATE_SMALL_CONFIRMING","HSBI_STATE_SMALL_CLOSING","HSBI_STATE_OLD_FAR_CLOSING",@J18,@J19,@J20,"HSBI_STATE_RETRY_PENDING","HSBI_STATE_RECONCILING","HSBI_STATE_EMERGENCY","HSBI_STATE_MANUAL_REVIEW","HSBI_STATE_TERMINAL_SAFE","HSBI_STATE_CYCLE_CLOSED"],KEY_ORDER=["From","To","PureTopologyAllowed","EventHandlerImplemented","RuntimeReachable","Event","Preconditions","StateEffect"],CONSTANTS={"EventHandlerImplemented":false,"RuntimeReachable":false,"Event":"NOT_AN_EVENT_API","Preconditions":@J21,"StateEffect":@J22},ROWS=["HSBI_STATE_DISABLED":110000000000000000000000000011010,"HSBI_STATE_IDLE":011000000000000000000000000011010,@J1:001100000000000000000000000011010,@J2:000110000000000000000000000011010,@J3:000011000000000000000000000011010,@J4:000001100000000000000000000011010,@J5:000000110000000000000000000011010,"HSBI_STATE_FAR_ACTIVE":000000011000000000000000000011010,@J6:000000001100000000000000000011010,@J7:000000000100000000000000000011010,@J8:000000000010000000000000000011010,@J9:000000000001000000000000000011010,"HSBI_STATE_BASKET_ACTIVE":000000000000100000000000000011010,@J10:000000000000010000000000000011010,@J11:000000000000001000000000000011010,@J12:000000000000000100000000000011010,@J13:000000000000000010000000000011010,@J14:000000000000000001000000000011010,@J15:000000000000000000100000000011010,@J16:000000000000000000010000000011010,@J17:000000000000000000001000000011010,"HSBI_STATE_SMALL_CONFIRMING":000000000000000000000100000011010,"HSBI_STATE_SMALL_CLOSING":000000000000000000000010000011010,"HSBI_STATE_OLD_FAR_CLOSING":000000000000000000000001000011010,@J18:000000000000000000000000100011010,@J19:000000000000000000000000010011010,@J20:000000000000000000000000001011010,"HSBI_STATE_RETRY_PENDING":000000000000000000000000000111010,"HSBI_STATE_RECONCILING":010000010000000000000000000011010,"HSBI_STATE_EMERGENCY":000000000000000000000000000011010,"HSBI_STATE_MANUAL_REVIEW":000000000000000000000000000011110,"HSBI_STATE_TERMINAL_SAFE":000000000000000000000000000011010,"HSBI_STATE_CYCLE_CLOSED":000000000000000000000000000011011]),"NormativeTransitions":[@T2("IDLE","INITIAL_LOCK_ACTIVE","Initial Lock fills","Persisted plan, two actual fills, ownership and fresh history",@J23,@J24,"UNIMPLEMENTED"),@T2("INITIAL_LOCK_ACTIVE","FAR_ACTIVE","Close InitialPlus completed","Independent economic record + actual remaining position",@J23,@J24,"UNIMPLEMENTED"),@T2("FAR_ACTIVE","BASKET_ACTIVE","Open C/T/S completed","Immutable candidate, volume/min/step, account margin, no pending",@J23,@J24,"UNIMPLEMENTED"),@T2("BASKET_ACTIVE","ALLOCATION_PENDING","Big Harvest completed","Actual BigCore/Trend deals, source attribution, full components",@J23,@J24,"UNIMPLEMENTED"),@T2("ALLOCATION_PENDING","FINAL_CLOSE_EXECUTING","FinalClose eligible","Realized+closeNow net threshold, no unknown/pending, fresh costs",@J23,@J24,"UNIMPLEMENTED"),@T2("ALLOCATION_PENDING","PARTIAL_FAR_EXECUTING","PartialFar eligible","Only PartialFarBudget owner reservation + actual loss",@J23,@J24,"UNIMPLEMENTED"),@T2("BASKET_ACTIVE","SMALL_CONFIRMING","Touch then hold/retrace","Fresh second snapshot, persisted debounce, no active transition",@J23,@J24,"UNIMPLEMENTED"),@T2("SMALL_CONFIRMING","OLD_FAR_CLOSING","Small close completed","Plan + actual Small deal + partial-fill barrier",@J23,@J24,"UNIMPLEMENTED"),@T2("OLD_FAR_CLOSING","BIG_TREND_CLOSING","OldFar close completed","Actual closure and no second Far",@J23,@J24,"UNIMPLEMENTED"),@T2("BIG_TREND_CLOSING","BIG_CORE_REDUCING","Trend close completed","Actual deal and cap/batch reconciliation",@J23,@J24,"UNIMPLEMENTED"),@T2("BIG_CORE_REDUCING","NEW_FAR_VALIDATING","Core partial complete","Original Core residual owner/id/volume confirmed",@J23,@J24,"UNIMPLEMENTED"),@T2("NEW_FAR_VALIDATING","FAR_ACTIVE","Promotion confirmed","All-level or explicit scope proofs + single actual Far",@J23,@J24,"UNIMPLEMENTED"),@T2("FINAL_CLOSE_EXECUTING","CYCLE_CLOSED","All positions closed","Actual final deals, ledger reconciliation, zero managed residual",@J23,@J24,"UNIMPLEMENTED"),@T2("ANY_PENDING","RECONCILING","Timeout/partial/out-of-order","No FSM advance until actual history and ownership reconciled",@J23,@J24,"UNIMPLEMENTED"),@T2("ANY","TERMINAL_SAFE","Critical unresolved conflict","No openings; manual authority required for restart/resume",@J23,@J24,"UNIMPLEMENTED")],"MainState":"DISABLED","Boundary":"Complete 33x33 pure-topology map, normative manual phase-level map only. Full normative event/precondition/action matrix not formally complete; audit remains PARTIAL."}
@T1=OBJECT_KEYS["From","To","PureTopologyAllowed","EventHandlerImplemented","RuntimeReachable","Event","Preconditions","StateEffect"]
@T2=OBJECT_KEYS["From","To","Event","Preconditions","Actions","Invariants","RuntimeStatus"]
@J1="HSBI_STATE_INITIAL_PLAN_READY"
@J2="HSBI_STATE_INITIAL_OPENING_BUY"
@J3="HSBI_STATE_INITIAL_OPENING_SELL"
@J4="HSBI_STATE_INITIAL_LOCK_ACTIVE"
@J5="HSBI_STATE_INITIAL_PLUS_CLOSING"
@J6="HSBI_STATE_CANDIDATE_PLANNED"
@J7="HSBI_STATE_BASKET_OPENING_CORE"
@J8="HSBI_STATE_BASKET_OPENING_TREND"
@J9="HSBI_STATE_BASKET_OPENING_SMALL"
@J10="HSBI_STATE_BIG_HARVEST_PLANNED"
@J11="HSBI_STATE_BIG_HARVEST_EXECUTING"
@J12="HSBI_STATE_ALLOCATION_PENDING"
@J13="HSBI_STATE_FINAL_CLOSE_PLANNED"
@J14="HSBI_STATE_FINAL_CLOSE_EXECUTING"
@J15="HSBI_STATE_PARTIAL_FAR_PLANNED"
@J16="HSBI_STATE_PARTIAL_FAR_EXECUTING"
@J17="HSBI_STATE_SMALL_TRANSITION_PLANNED"
@J18="HSBI_STATE_BIG_TREND_CLOSING"
@J19="HSBI_STATE_BIG_CORE_REDUCING"
@J20="HSBI_STATE_NEW_FAR_VALIDATING"
@J21="Topology only; no deals/ownership/timeouts/resume authority"
@J22="Pure helper can change context/revision if called; main never calls it"
@J23="Desired transaction→actual history→ledger→persist→FSM; UNIMPLEMENTED event orchestration"
@J24="SingleFar, no double-funding, exact owner/replay, fresh independent facts"
```


## C2 catalog — exact string sequence notation

@STRING_SEQUENCE(prefix,first,last,step1) используется только когда всеисходныеэлементысутьточныеJSONстроки prefix+str(n),безleadingzero/gaps/перестановок. Неудаляет2462ID: ониперечисленывзамкнутомгенераторе иобратновосстановимы. Guards/Mutations/Testsпрочитаныполностью;схемаIDsнесодержитвходовschema-probes,толькореестрназваний. 60731символwholeview:первые36000originalfactoredview,затемoverlap26000–42000и42000–60731sequenceview. Ниодинguard/testнеисполнялся.

```text
ROOT={"BaseSHA":"fae7dfc18ca2d61af2f3446826ef3031825bbfd8","CatalogVersion":"HSBI-C2-REQUIRED-1","Guards":[@T1("C2-C1-MUT-raw-sum","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-raw-sum","C2-C1-MUT-raw-sum","C2-BASE-SOURCE-raw","C2-BASE-SOURCE-positive",null,"economic_record"),@T1("C2-C1-MUT-posted-grid","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-posted-grid","C2-C1-MUT-posted-grid","C2-BASE-RECORD-grid","C2-BASE-SOURCE-positive",null,"economic_record"),@T1("C2-C1-MUT-source-namespace","C2-SCHEMA-AND-BINDING",@J1,@J2,"C2-C1-MUT-source-namespace","C2-BASE-SOURCE-namespace","C2-BASE-SOURCE-positive",null,"economic_record"),@T1("C2-C1-MUT-balance-reserved","C2-SCHEMA-AND-BINDING",@J1,@J3,"C2-C1-MUT-balance-reserved","C2-BASE-BALANCE-doublecount","C2-BASE-BALANCE-no-reserve",null,"balance"),@T1("C2-C1-MUT-source-cap","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-source-cap","C2-C1-MUT-source-cap","C2-BASE-SOURCE-overfund","C2-BASE-SOURCE-positive",null,"_fund"),@T1("C2-C1-MUT-small-role","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-small-role","C2-C1-MUT-small-role","C2-BASE-SOURCE-small","C2-BASE-SOURCE-positive",null,"_fund"),@T1("C2-C1-MUT-projected-source","C2-SCHEMA-AND-BINDING",@J1,@J4,"C2-C1-MUT-projected-source","C2-BASE-SOURCE-projected","C2-BASE-SOURCE-positive",null,"economic_record"),@T1("C2-C1-MUT-fund-replay","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-fund-replay","C2-C1-MUT-fund-replay","C2-BASE-FUND-changed","C2-BASE-FUND-exact",null,"_event"),@T1(@J5,"C2-SCHEMA-AND-BINDING",@J1,@J6,@J5,@J7,"C2-BASE-FUND-exact",null,"_fund"),@T1("C2-C1-MUT-identity-Broker","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-identity-Broker","C2-C1-MUT-identity-Broker",@J8,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-identity-Server","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-identity-Server","C2-C1-MUT-identity-Server",@J9,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-identity-Account","C2-SCHEMA-AND-BINDING",@J1,@J10,"C2-C1-MUT-identity-Account",@J11,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-identity-Symbol","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-identity-Symbol","C2-C1-MUT-identity-Symbol",@J12,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-identity-Magic","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-identity-Magic","C2-C1-MUT-identity-Magic",@J13,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-identity-Cycle","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-identity-Cycle","C2-C1-MUT-identity-Cycle",@J14,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-identity-Position","C2-SCHEMA-AND-BINDING",@J1,@J15,"C2-C1-MUT-identity-Position",@J16,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-identity-Deal","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-identity-Deal","C2-C1-MUT-identity-Deal",@J17,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-identity-Order","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-identity-Order","C2-C1-MUT-identity-Order",@J18,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-identity-Role","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-identity-Role","C2-C1-MUT-identity-Role",@J19,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1(@J20,"C2-SCHEMA-AND-BINDING",@J1,@J21,@J20,@J22,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1(@J23,"C2-SCHEMA-AND-BINDING",@J1,@J24,@J23,@J25,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1(@J26,"C2-SCHEMA-AND-BINDING",@J1,@J27,@J26,@J28,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1(@J29,"C2-SCHEMA-AND-BINDING",@J1,@J30,@J29,@J31,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1(@J32,"C2-SCHEMA-AND-BINDING",@J1,@J33,@J32,@J34,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-identity-Plan","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-identity-Plan","C2-C1-MUT-identity-Plan",@J35,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-identity-Revision","C2-SCHEMA-AND-BINDING",@J1,@J36,"C2-C1-MUT-identity-Revision",@J37,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-identity-Snapshot","C2-SCHEMA-AND-BINDING",@J1,@J38,"C2-C1-MUT-identity-Snapshot",@J39,"C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-batch-namespace","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-batch-namespace","C2-C1-MUT-batch-namespace",@J40,"C2-BASE-BATCH-control",null,"assess_batch"),@T1("C2-C1-MUT-batch-lineage","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-batch-lineage","C2-C1-MUT-batch-lineage","C2-BASE-BATCH-foreign-Order","C2-BASE-BATCH-control",null,"assess_batch"),@T1(@J41,"C2-SCHEMA-AND-BINDING",@J1,@J42,@J41,"C2-BASE-BATCH-pending","C2-BASE-BATCH-control",null,"assess_batch"),@T1("C2-C1-MUT-cost-inventory","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-cost-inventory","C2-C1-MUT-cost-inventory","C2-BASE-COST-missing","C2-BASE-COST-control",null,"cost_coverage"),@T1("C2-C1-MUT-cost-once","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-cost-once","C2-C1-MUT-cost-once","C2-BASE-COST-omitted","C2-BASE-COST-control",null,"cost_coverage"),@T1(@J43,"C2-SCHEMA-AND-BINDING",@J1,@J44,@J43,@J45,"C2-BASE-AVAILABLE-control",null,"available"),@T1("C2-C1-MUT-composition-batch","C2-SCHEMA-AND-BINDING",@J1,@J46,"C2-C1-MUT-composition-batch","C2-BASE-APPLY-bypass-batch","C2-BASE-APPLY-positive",null,"_authorize"),@T1("C2-C1-MUT-composition-cost","C2-SCHEMA-AND-BINDING",@J1,@J47,"C2-C1-MUT-composition-cost","C2-BASE-APPLY-bypass-cost","C2-BASE-APPLY-positive",null,"_authorize"),@T1("C2-C1-MUT-planned-operation","C2-SCHEMA-AND-BINDING",@J1,@J48,"C2-C1-MUT-planned-operation",@J49,"C2-BASE-APPLY-positive",null,"_authorize"),@T1("C2-C1-MUT-composed-replay","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-composed-replay","C2-C1-MUT-composed-replay","C2-BASE-REPLAY-changed","C2-BASE-REPLAY-exact",null,"_authorize"),@T1(@J50,"C2-SCHEMA-AND-BINDING",@J1,@J51,@J50,"C2-BASE-REPLAY-authority","C2-BASE-REPLAY-exact",null,"_authorize"),@T1(@J52,"C2-SCHEMA-AND-BINDING",@J1,@J53,@J52,@J54,"C2-BASE-APPLY-positive",null,"apply_for_test"),@T1("C2-C1-MUT-outer-poststate","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-outer-poststate","C2-C1-MUT-outer-poststate",@J55,"C2-BASE-APPLY-positive",@J56,"apply_for_test"),@T1("C2-C1-MUT-snapshot-fresh","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-snapshot-fresh","C2-C1-MUT-snapshot-fresh","C2-BASE-IDENTITY-stale","C2-BASE-IDENTITY-control",null,"verify_allocation_identity"),@T1("C2-C1-MUT-batch-policy","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-batch-policy","C2-C1-MUT-batch-policy",@J57,"C2-BASE-BATCH-control",null,"assess_batch"),@T1(@J58,"C2-SCHEMA-AND-BINDING",@J1,@J59,@J58,@J60,"C2-BASE-COST-control",null,"cost_coverage"),@T1("C2-C1-MUT-cost-headroom","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-cost-headroom","C2-C1-MUT-cost-headroom",@J61,"C2-BASE-APPLY-positive",null,"_authorize"),@T1("C2-C1-MUT-receipt-inventory","C2-SCHEMA-AND-BINDING",@J1,@J62,"C2-C1-MUT-receipt-inventory","C2-BASE-RECOVER-no-receipt","C2-BASE-RECOVER-control",null,"_reconcile_store"),@T1("C2-C1-MUT-receipt-source","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-receipt-source","C2-C1-MUT-receipt-source",@J63,"C2-BASE-RECOVER-control",null,"_reconcile_store"),@T1(@J64,"C2-SCHEMA-AND-BINDING",@J1,@J65,@J64,@J66,"C2-BASE-IDENTITY-control",@J67,"verify_allocation_identity"),@T1(@J68,"C2-SCHEMA-AND-BINDING",@J1,@J69,@J68,@J70,"C2-BASE-RECOVER-control",null,"_reconcile_store"),@T1(@J71,"C2-SCHEMA-AND-BINDING",@J1,@J72,@J71,@J73,"C2-BASE-RECOVER-control",null,"_reconcile_store"),@T1("C2-C1-MUT-historical-plan","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-historical-plan","C2-C1-MUT-historical-plan",@J74,"C2-BASE-RECOVER-control",null,"_reconcile_store"),@T1("C2-C1-MUT-digest-format","C2-SCHEMA-AND-BINDING",@J1,"C2-C1-GUARD-digest-format","C2-C1-MUT-digest-format",@J75,"C2-BASE-RECOVER-control",@J67,"_reconcile_store"),@T1(@J76,"C2-SCHEMA-AND-BINDING",@J1,@J77,@J76,@J78,"C2-BASE-APPLY-positive",@J67,"_reconcile_store"),@T1(@J79,"C2-SCHEMA-AND-BINDING",@J1,@J80,@J79,@J81,"C2-BASE-APPLY-positive",@J67,"_authorize"),@T1("C2-MUT-receipt-digest","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-receipt-digest","C2-MUT-receipt-digest","C2-receipt-digest","C2-BASE-RECOVER-control",null,"_reconcile_store"),@T1("C2-MUT-receipt-equation","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-receipt-equation","C2-MUT-receipt-equation","C2-receipt-equation","C2-BASE-RECOVER-control",null,"_reconcile_store"),@T1("C2-MUT-planned-purpose","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-planned-purpose","C2-MUT-planned-purpose","C2-planned-purpose","C2-BASE-APPLY-positive",null,"_authorize"),@T1("C2-MUT-planned-intent","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-planned-intent","C2-MUT-planned-intent","C2-planned-intent","C2-BASE-APPLY-positive",null,"_authorize"),@T1("C2-MUT-ledger-event","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-ledger-event","C2-MUT-ledger-event","C2-ledger-allocationEvent","C2-BASE-APPLY-positive",null,"_bind_allocation"),@T1("C2-MUT-ledger-policy","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-ledger-policy","C2-MUT-ledger-policy","C2-ledger-PolicyVersion","C2-BASE-APPLY-positive",null,"_bind_allocation"),@T1(@J82,"C2-SCHEMA-AND-BINDING",@J1,@J83,@J82,@J84,"C2-BASE-RECOVER-control",null,"_reconcile_store"),@T1("C2-MUT-receipt-principal","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-receipt-principal","C2-MUT-receipt-principal","C2-receipt-clause-principal","C2-BASE-RECOVER-control",null,"_reconcile_store"),@T1("C2-MUT-receipt-core-debit","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-receipt-core-debit","C2-MUT-receipt-core-debit","C2-receipt-clause-core","C2-BASE-RECOVER-control",null,"_reconcile_store"),@T1("C2-MUT-cost-shape-caller","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-cost-shape-caller","C2-MUT-cost-shape-caller","C2-cost-bool-direct","C2-BASE-COST-control",@J85,"cost_coverage"),@T1(@J86,"C2-SCHEMA-AND-BINDING",@J1,@J87,@J86,"C2-cost-bool-direct","C2-BASE-COST-control",null,"cost_coverage"),@T1("C2-MUT-bool-id","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-bool-id","C2-MUT-bool-id","C2-bool-policy","C2-BASE-APPLY-positive",null,"validate"),@T1("C2-MUT-unknown-fields","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-unknown-fields","C2-MUT-unknown-fields","C2-schema-unknown-field","C2-BASE-COST-control",null,"validate"),@T1(@J88,"C2-SCHEMA-AND-BINDING",@J1,@J89,@J88,@J90,"C2-BASE-APPLY-positive",null,"_authorize"),@T1("C2-MUT-json-last-wins","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-json-last-wins","C2-MUT-json-last-wins","C2-JSON-duplicate","C2-JSON-control",null,"pairs"),@T1("C2-MUT-json-constants","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-json-constants","C2-MUT-json-constants","C2-JSON-nan","C2-JSON-control",null,"loads"),@T1("C2-MUT-json-counter-bool","C2-SCHEMA-AND-BINDING",@J1,"C2-GUARD-json-counter-bool","C2-MUT-json-counter-bool","C2-JSON-counter","C2-JSON-control",null,"integer")],"Mutations":[@T2([{"new":"","old":"raw==number(r['rawNet']) and "}],"KILL","C2-C1-GUARD-raw-sum","C2-C1-MUT-raw-sum","C2-BASE-SOURCE-raw","C2-BASE-SOURCE-positive",null,@J91,"economic_record"),@T2([{"new":"","old":" and exact.grid(r['postedNet'],r['digits'])"}],"KILL","C2-C1-GUARD-posted-grid","C2-C1-MUT-posted-grid","C2-BASE-RECORD-grid","C2-BASE-SOURCE-positive",null,@J91,"economic_record"),@T2([{"new":"require(True)","old":"require(source_key(r)==tuple(source))"}],"KILL",@J2,"C2-C1-MUT-source-namespace","C2-BASE-SOURCE-namespace","C2-BASE-SOURCE-positive",null,@J91,"economic_record"),@T2([{"new":"g!=c+f","old":"g!=c+v+f"}],"KILL",@J3,"C2-C1-MUT-balance-reserved","C2-BASE-BALANCE-doublecount","C2-BASE-BALANCE-no-reserve",null,@J91,"balance"),@T2([{"new":"if False:","old":"if total>net:"}],"KILL","C2-C1-GUARD-source-cap","C2-C1-MUT-source-cap","C2-BASE-SOURCE-overfund","C2-BASE-SOURCE-positive",null,@J91,"_fund"),@T2([{"new":"if False:","old":"if role=='Small' and any(values[b]!=0 for b in BUCKETS if b!='ResidualHeld'):"}],"KILL","C2-C1-GUARD-small-role","C2-C1-MUT-small-role","C2-BASE-SOURCE-small","C2-BASE-SOURCE-positive",null,@J91,"_fund"),@T2([{"new":"if False:","old":"if r['kind']!='ReconciledEconomicNet':"}],"KILL",@J4,"C2-C1-MUT-projected-source","C2-BASE-SOURCE-projected","C2-BASE-SOURCE-positive",null,@J91,"economic_record"),@T2([{"new":"'NO_OP'","old":"('NO_OP' if canonical(prior['payload'])==canonical(payload) else 'CONFLICT')"}],"KILL","C2-C1-GUARD-fund-replay","C2-C1-MUT-fund-replay","C2-BASE-FUND-changed","C2-BASE-FUND-exact",null,@J91,"_event"),@T2([{"new":"if False:","old":"if old_source and old_source['recordDigest']!=digest(r):"}],"KILL",@J6,@J5,@J7,"C2-BASE-FUND-exact",null,@J91,"_fund"),@T2([{"new":"for k in expected if k!='Broker') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL","C2-C1-GUARD-identity-Broker","C2-C1-MUT-identity-Broker",@J8,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='Server') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL","C2-C1-GUARD-identity-Server","C2-C1-MUT-identity-Server",@J9,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='Account') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL",@J10,"C2-C1-MUT-identity-Account",@J11,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='Symbol') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL","C2-C1-GUARD-identity-Symbol","C2-C1-MUT-identity-Symbol",@J12,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='Magic') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL","C2-C1-GUARD-identity-Magic","C2-C1-MUT-identity-Magic",@J13,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='Cycle') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL","C2-C1-GUARD-identity-Cycle","C2-C1-MUT-identity-Cycle",@J14,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='Position') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL",@J15,"C2-C1-MUT-identity-Position",@J16,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='Deal') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL","C2-C1-GUARD-identity-Deal","C2-C1-MUT-identity-Deal",@J17,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='Order') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL","C2-C1-GUARD-identity-Order","C2-C1-MUT-identity-Order",@J18,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='Role') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL","C2-C1-GUARD-identity-Role","C2-C1-MUT-identity-Role",@J19,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='EconomicEventID') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL",@J21,@J20,@J22,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='AllocationEventID') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL",@J24,@J23,@J25,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='ConsumptionEventID') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL",@J27,@J26,@J28,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='AllocationID') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL",@J30,@J29,@J31,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='PolicyVersion') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL",@J33,@J32,@J34,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='Plan') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL","C2-C1-GUARD-identity-Plan","C2-C1-MUT-identity-Plan",@J35,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='Revision') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL",@J36,"C2-C1-MUT-identity-Revision",@J37,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"for k in expected if k!='Snapshot') else 'REJECT'  # GUARD:C1-IDENTITY","old":@J92}],"KILL",@J38,"C2-C1-MUT-identity-Snapshot",@J39,"C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"require(True)","old":"require(k[:3]==(expected['Broker'],expected['Server'],expected['Account']))"}],"KILL","C2-C1-GUARD-batch-namespace","C2-C1-MUT-batch-namespace",@J40,"C2-BASE-BATCH-control",null,@J91,"assess_batch"),@T2([{"new":"require(True)","old":"require(all(type(fill[f]) is type(expected[f]) and fill[f]==expected[f] for f in ('BatchID','Symbol','Cycle','Order','Position','currency','digits')))"}],"KILL","C2-C1-GUARD-batch-lineage","C2-C1-MUT-batch-lineage","C2-BASE-BATCH-foreign-Order","C2-BASE-BATCH-control",null,@J91,"assess_batch"),@T2([{"new":"if False:","old":"if unique!=set(required) or volume!=planned:"}],"KILL",@J42,@J41,"C2-BASE-BATCH-pending","C2-BASE-BATCH-control",null,@J91,"assess_batch"),@T2([{"new":"require(True)","old":"require(len(set(ids))==len(ids) and set(ids)==set(facts))"}],"KILL","C2-C1-GUARD-cost-inventory","C2-C1-MUT-cost-inventory","C2-BASE-COST-missing","C2-BASE-COST-control",null,@J91,"cost_coverage"),@T2([{"new":"require(True)","old":"require(row['AdditionalDeduction']==needed)"}],"KILL","C2-C1-GUARD-cost-once","C2-C1-MUT-cost-once","C2-BASE-COST-omitted","C2-BASE-COST-control",null,@J91,"cost_coverage"),@T2([{"new":"pass\n        return _arithmetic_reserve_balance","old":"_reconcile_store(store,authority)\n        return _arithmetic_reserve_balance"}],"KILL",@J44,@J43,@J45,"C2-BASE-AVAILABLE-control",null,@J91,"available"),@T2([{"new":"if False:","old":"if assessment['status']!='CONFIRMED':"}],"KILL",@J46,"C2-C1-MUT-composition-batch","C2-BASE-APPLY-bypass-batch","C2-BASE-APPLY-positive",null,@J91,"_authorize"),@T2([{"new":"if costs['status']!='COVERED':costs=_answer('COVERED',AdditionalRisk=Fraction(0))","old":"if costs['status']!='COVERED':return _answer('REJECT' if costs['status']=='CONFLICT' else 'UNAVAILABLE')"}],"KILL",@J47,"C2-C1-MUT-composition-cost","C2-BASE-APPLY-bypass-cost","C2-BASE-APPLY-positive",null,@J91,"_authorize"),@T2([{"new":"require(True)","old":"require(number(context['PrincipalAmount'])==number(q['PrincipalAmount']) and all(context[k]==q[k] for k in ('bucket','purpose','intent')))"}],"KILL",@J48,"C2-C1-MUT-planned-operation",@J49,"C2-BASE-APPLY-positive",null,@J91,"_authorize"),@T2([{"new":"_answer('NO_OP')","old":"_answer('NO_OP' if canonical(prior['request'])==canonical(q) else 'CONFLICT')"}],"KILL","C2-C1-GUARD-composed-replay","C2-C1-MUT-composed-replay","C2-BASE-REPLAY-changed","C2-BASE-REPLAY-exact",null,@J91,"_authorize"),@T2([{"new":"if False:","old":"if known is not None and known['recordDigest']!=digest(r):"}],"KILL",@J51,@J50,"C2-BASE-REPLAY-authority","C2-BASE-REPLAY-exact",null,@J91,"_authorize"),@T2([{"new":"result=_answer('ELIGIBLE_FOR_COMMIT',DebitAmount=number(q['PrincipalAmount']),RequiredBalance=number(q['PrincipalAmount']),AdditionalRisk=Fraction(0),sourceDigest=digest(economic_record(authority['history'],q['source'])),allocationDigest=digest(authority['allocations'][q['allocation']]),batchDigest=digest(authority['batches'][q['BatchID']]),costDigest=digest(authority['costSets'][q['CostSetID']]))","old":"result=authorize(q,store,authority)"}],"KILL",@J53,@J52,@J54,"C2-BASE-APPLY-positive",null,@J91,"apply_for_test"),@T2([{"new":"if False:return _answer('UNAVAILABLE'),copy.deepcopy(store)","old":"if not balance(b['OriginalGrant'],b['Consumed'],b['Reserved'],b['RemainingFree'],b['Reservations']):return _answer('UNAVAILABLE'),copy.deepcopy(store)"}],"REDUNDANT_GUARD_SURVIVOR","C2-C1-GUARD-outer-poststate","C2-C1-MUT-outer-poststate",@J55,"C2-BASE-APPLY-positive",@J56,@J91,"apply_for_test"),@T2([{"new":"if False:return 'UNAVAILABLE'\n        require(context['AllocationID']","old":"if not context['fresh']:return 'UNAVAILABLE'\n        require(context['AllocationID']"}],"KILL","C2-C1-GUARD-snapshot-fresh","C2-C1-MUT-snapshot-fresh","C2-BASE-IDENTITY-stale","C2-BASE-IDENTITY-control",null,@J91,"verify_allocation_identity"),@T2([{"new":"if False:","old":"if not expected['historyComplete'] or expected['NettingPolicy']!='PROPOSED_SIGNED_BATCH_NET_V1':"}],"KILL","C2-C1-GUARD-batch-policy","C2-C1-MUT-batch-policy",@J57,"C2-BASE-BATCH-control",null,@J91,"assess_batch"),@T2([{"new":"if False:","old":"if not expected['Complete']:"}],"KILL",@J59,@J58,@J60,"C2-BASE-COST-control",null,@J91,"cost_coverage"),@T2([{"new":"number(q['PrincipalAmount'])","old":"number(q['PrincipalAmount'])+costs['AdditionalRisk']"}],"KILL","C2-C1-GUARD-cost-headroom","C2-C1-MUT-cost-headroom",@J61,"C2-BASE-APPLY-positive",null,@J91,"_authorize"),@T2([{"new":"require(True)","old":"require(set(store['receipts'])==needed)"}],"KILL",@J62,"C2-C1-MUT-receipt-inventory","C2-BASE-RECOVER-no-receipt","C2-BASE-RECOVER-control",null,@J91,"_reconcile_store"),@T2([{"new":"require(True)","old":"require(receipt['sourceDigest']==store['ledger']['sources'][key(q['source'])]['recordDigest'])"}],"KILL","C2-C1-GUARD-receipt-source","C2-C1-MUT-receipt-source",@J63,"C2-BASE-RECOVER-control",null,@J91,"_reconcile_store"),@T2([{"new":"require(allocation['source']==source)","old":"require(type(presented) is dict and allocation['source']==source)"},{"new":"presented=copy.deepcopy(expected) if presented is None else presented\n        require(set(presented)==set(expected))","old":"require(set(presented)==set(expected))"}],"REDUNDANT_GUARD_SURVIVOR",@J65,@J64,@J66,"C2-BASE-IDENTITY-control",@J67,@J91,"verify_allocation_identity"),@T2([{"new":"require(True)","old":"require(q['allocationEvent']==historical['allocationEvent'] and receipt['allocationDigest']==digest(historical))"}],"KILL",@J69,@J68,@J70,"C2-BASE-RECOVER-control",null,@J91,"_reconcile_store"),@T2([{"new":"require(True)","old":"require(verify_allocation_identity(q['identity'],authority['history'],q['source'],ctx,historical)=='PASS')"}],"KILL",@J72,@J71,@J73,"C2-BASE-RECOVER-control",null,@J91,"_reconcile_store"),@T2([{"new":"require(True)","old":"require((ctx['ConsumptionEventID'],ctx['Revision'],number(ctx['PrincipalAmount']),ctx['bucket'],ctx['purpose'],ctx['intent'],ctx['BatchID'],ctx['CostSetID'])==(q['consumptionEvent'],q['revision'],number(q['PrincipalAmount']),q['bucket'],q['purpose'],q['intent'],q['BatchID'],q['CostSetID']))"}],"KILL","C2-C1-GUARD-historical-plan","C2-C1-MUT-historical-plan",@J74,"C2-BASE-RECOVER-control",null,@J91,"_reconcile_store"),@T2([{"new":"","old":" and all(c in '0123456789abcdef' for c in receipt[field])"}],"REDUNDANT_GUARD_SURVIVOR","C2-C1-GUARD-digest-format","C2-C1-MUT-digest-format",@J75,"C2-BASE-RECOVER-control",@J67,@J91,"_reconcile_store"),@T2([{"new":"if any(type(e) is not dict for e in authority['coreJournal'].values()):authority['coreJournal']=copy.deepcopy(store['ledger']['events'])","old":"_validate_core_journal(authority['coreJournal'])"}],"REDUNDANT_GUARD_SURVIVOR",@J77,@J76,@J78,"C2-BASE-APPLY-positive",@J67,@J91,"_reconcile_store"),@T2([{"new":"if type(known) is not dict:known=None","old":"if known is not None:\n        exact.fields(known,('source','recordDigest','granted','net','phase','unallocated'));require(type(known['recordDigest']) is str)"}],"REDUNDANT_GUARD_SURVIVOR",@J80,@J79,@J81,"C2-BASE-APPLY-positive",@J67,@J91,"_authorize"),@T2([{"new":"","old":"receipt['digest']==digest(q) and "}],"KILL","C2-GUARD-receipt-digest","C2-MUT-receipt-digest","C2-receipt-digest","C2-BASE-RECOVER-control",null,@J91,"_reconcile_store"),@T2([{"new":"require(True)","old":"require(number(receipt['AdditionalRisk'])>=0 and number(receipt['DebitAmount'])==number(q['PrincipalAmount']) and number(receipt['RequiredBalance'])==number(receipt['DebitAmount'])+number(receipt['AdditionalRisk']) and number(e['amount'])==number(receipt['DebitAmount']))"}],"KILL","C2-GUARD-receipt-equation","C2-MUT-receipt-equation","C2-receipt-equation","C2-BASE-RECOVER-control",null,@J91,"_reconcile_store"),@T2([{"new":"for k in ('bucket','intent')","old":@J93}],"KILL","C2-GUARD-planned-purpose","C2-MUT-planned-purpose","C2-planned-purpose","C2-BASE-APPLY-positive",null,@J91,"_authorize"),@T2([{"new":"for k in ('bucket','purpose')","old":@J93}],"KILL","C2-GUARD-planned-intent","C2-MUT-planned-intent","C2-planned-intent","C2-BASE-APPLY-positive",null,@J91,"_authorize"),@T2([{"new":"","old":" and ledger['allocationEvent']==record['allocationEvent']"}],"KILL","C2-GUARD-ledger-event","C2-MUT-ledger-event","C2-ledger-allocationEvent","C2-BASE-APPLY-positive",null,@J91,"_bind_allocation"),@T2([{"new":"","old":" and ledger['policyVersion']==record['PolicyVersion']"}],"KILL","C2-GUARD-ledger-policy","C2-MUT-ledger-policy","C2-ledger-PolicyVersion","C2-BASE-APPLY-positive",null,@J91,"_bind_allocation"),@T2([{"new":"","old":"number(receipt['AdditionalRisk'])>=0 and "}],"KILL",@J83,@J82,@J84,"C2-BASE-RECOVER-control",null,@J91,"_reconcile_store"),@T2([{"new":"","old":"number(receipt['DebitAmount'])==number(q['PrincipalAmount']) and "}],"KILL","C2-GUARD-receipt-principal","C2-MUT-receipt-principal","C2-receipt-clause-principal","C2-BASE-RECOVER-control",null,@J91,"_reconcile_store"),@T2([{"new":"","old":" and number(e['amount'])==number(receipt['DebitAmount'])"}],"KILL","C2-GUARD-receipt-core-debit","C2-MUT-receipt-core-debit","C2-receipt-clause-core","C2-BASE-RECOVER-control",null,@J91,"_reconcile_store"),@T2([@J95],"REDUNDANT_GUARD_SURVIVOR","C2-GUARD-cost-shape-caller","C2-MUT-cost-shape-caller","C2-cost-bool-direct","C2-BASE-COST-control",@J85,@J91,"cost_coverage"),@T2([@J95,{"new":"pass","old":"dto.validate({\"list\":\"CostClaim\"},rows)"}],"KILL",@J87,@J86,"C2-cost-bool-direct","C2-BASE-COST-control",null,@J91,"cost_coverage"),@T2([{"new":"elif spec=='uid':x.require(x.uid(value) or type(value) is bool)","old":"elif spec=='uid':x.require(x.uid(value))"}],"KILL","C2-GUARD-bool-id","C2-MUT-bool-id","C2-bool-policy","C2-BASE-APPLY-positive",null,@J96,"validate"),@T2([{"new":"x.require(type(value) is dict and set(spec['object'])<=value.keys())","old":"x.fields(value,tuple(spec['object']))"}],"KILL","C2-GUARD-unknown-fields","C2-MUT-unknown-fields","C2-schema-unknown-field","C2-BASE-COST-control",null,@J96,"validate"),@T2([{"new":"pass","old":"if a is not None:dto.validate(\"Authority\",a)"},{"new":"pass","old":"if authority is not None:dto.validate(\"Authority\",authority)"}],"KILL",@J89,@J88,@J90,"C2-BASE-APPLY-positive",null,@J91,"_authorize"),@T2([{"new":"if False:raise ValueError('duplicate JSON key: '+k)","old":"if k in out:raise ValueError('duplicate JSON key: '+k)"}],"KILL","C2-GUARD-json-last-wins","C2-MUT-json-last-wins","C2-JSON-duplicate","C2-JSON-control",null,@J97,"pairs"),@T2([{"new":"parse_constant=lambda x:None","old":"parse_constant=constant"}],"KILL","C2-GUARD-json-constants","C2-MUT-json-constants","C2-JSON-nan","C2-JSON-control",null,@J97,"loads"),@T2([{"new":"if not isinstance(value,int):","old":"if type(value) is not int:"}],"KILL","C2-GUARD-json-counter-bool","C2-MUT-json-counter-bool","C2-JSON-counter","C2-JSON-control",null,@J97,"integer")],"RequiredGuardIDs":["C2-C1-GUARD-raw-sum","C2-C1-GUARD-posted-grid",@J2,@J3,"C2-C1-GUARD-source-cap","C2-C1-GUARD-small-role",@J4,"C2-C1-GUARD-fund-replay",@J6,"C2-C1-GUARD-identity-Broker","C2-C1-GUARD-identity-Server",@J10,"C2-C1-GUARD-identity-Symbol","C2-C1-GUARD-identity-Magic","C2-C1-GUARD-identity-Cycle",@J15,"C2-C1-GUARD-identity-Deal","C2-C1-GUARD-identity-Order","C2-C1-GUARD-identity-Role",@J21,@J24,@J27,@J30,@J33,"C2-C1-GUARD-identity-Plan",@J36,@J38,"C2-C1-GUARD-batch-namespace","C2-C1-GUARD-batch-lineage",@J42,"C2-C1-GUARD-cost-inventory","C2-C1-GUARD-cost-once",@J44,@J46,@J47,@J48,"C2-C1-GUARD-composed-replay",@J51,@J53,"C2-C1-GUARD-outer-poststate","C2-C1-GUARD-snapshot-fresh","C2-C1-GUARD-batch-policy",@J59,"C2-C1-GUARD-cost-headroom",@J62,"C2-C1-GUARD-receipt-source",@J65,@J69,@J72,"C2-C1-GUARD-historical-plan","C2-C1-GUARD-digest-format",@J77,@J80,"C2-GUARD-receipt-digest","C2-GUARD-receipt-equation","C2-GUARD-planned-purpose","C2-GUARD-planned-intent","C2-GUARD-ledger-event","C2-GUARD-ledger-policy",@J83,"C2-GUARD-receipt-principal","C2-GUARD-receipt-core-debit","C2-GUARD-cost-shape-caller",@J87,"C2-GUARD-bool-id","C2-GUARD-unknown-fields",@J89,"C2-GUARD-json-last-wins","C2-GUARD-json-constants","C2-GUARD-json-counter-bool"],"RequiredMutationIDs":["C2-C1-MUT-raw-sum","C2-C1-MUT-posted-grid","C2-C1-MUT-source-namespace","C2-C1-MUT-balance-reserved","C2-C1-MUT-source-cap","C2-C1-MUT-small-role","C2-C1-MUT-projected-source","C2-C1-MUT-fund-replay",@J5,"C2-C1-MUT-identity-Broker","C2-C1-MUT-identity-Server","C2-C1-MUT-identity-Account","C2-C1-MUT-identity-Symbol","C2-C1-MUT-identity-Magic","C2-C1-MUT-identity-Cycle","C2-C1-MUT-identity-Position","C2-C1-MUT-identity-Deal","C2-C1-MUT-identity-Order","C2-C1-MUT-identity-Role",@J20,@J23,@J26,@J29,@J32,"C2-C1-MUT-identity-Plan","C2-C1-MUT-identity-Revision","C2-C1-MUT-identity-Snapshot","C2-C1-MUT-batch-namespace","C2-C1-MUT-batch-lineage",@J41,"C2-C1-MUT-cost-inventory","C2-C1-MUT-cost-once",@J43,"C2-C1-MUT-composition-batch","C2-C1-MUT-composition-cost","C2-C1-MUT-planned-operation","C2-C1-MUT-composed-replay",@J50,@J52,"C2-C1-MUT-outer-poststate","C2-C1-MUT-snapshot-fresh","C2-C1-MUT-batch-policy",@J58,"C2-C1-MUT-cost-headroom","C2-C1-MUT-receipt-inventory","C2-C1-MUT-receipt-source",@J64,@J68,@J71,"C2-C1-MUT-historical-plan","C2-C1-MUT-digest-format",@J76,@J79,"C2-MUT-receipt-digest","C2-MUT-receipt-equation","C2-MUT-planned-purpose","C2-MUT-planned-intent","C2-MUT-ledger-event","C2-MUT-ledger-policy",@J82,"C2-MUT-receipt-principal","C2-MUT-receipt-core-debit","C2-MUT-cost-shape-caller",@J86,"C2-MUT-bool-id","C2-MUT-unknown-fields",@J88,"C2-MUT-json-last-wins","C2-MUT-json-constants","C2-MUT-json-counter-bool"],"RequiredSchemaProbeIDs":@STRING_SEQUENCE(prefix="C2-SCHEMA-",first=1,last=2462,step=1),"RequiredTestIDs":["C2-BASE-APPLY-positive","C2-BASE-SOURCE-positive","C2-BASE-SOURCE-raw","C2-BASE-SOURCE-namespace","C2-BASE-SOURCE-grid","C2-BASE-RECORD-grid","C2-BASE-BALANCE-control","C2-BASE-BALANCE-doublecount","C2-BASE-APPLY-no-journal","C2-BASE-AVAILABLE-control",@J98,@J99,@J55,"C2-BASE-IDENTITY-control",@J8,@J9,@J11,@J12,@J13,@J14,@J16,@J17,@J18,@J19,@J22,@J25,@J28,@J31,@J34,@J35,@J37,@J39,@J100,@J66,@J101,@J102,"C2-BASE-IDENTITY-stale","C2-BASE-BATCH-control",@J40,@J103,@J104,"C2-BASE-BATCH-foreign-Cycle","C2-BASE-BATCH-foreign-Order",@J105,@J106,@J107,"C2-BASE-BATCH-pending","C2-BASE-BATCH-overcap",@J57,"C2-BASE-COST-control","C2-BASE-COST-missing","C2-BASE-COST-omitted","C2-BASE-COST-unknown","C2-BASE-COST-duplicate","C2-BASE-COST-knownzero","C2-BASE-COST-knownempty","C2-BASE-APPLY-bypass-batch","C2-BASE-APPLY-bypass-cost",@J54,@J49,@J108,@J61,"C2-BASE-APPLY-full","C2-BASE-REPLAY-exact","C2-BASE-REPLAY-changed","C2-BASE-REPLAY-authority",@J109,"C2-BASE-RECOVER-control","C2-BASE-RECOVER-forged","C2-BASE-BALANCE-no-reserve","C2-BASE-SOURCE-overfund","C2-BASE-SOURCE-small","C2-BASE-SOURCE-projected","C2-BASE-FUND-exact","C2-BASE-FUND-changed",@J7,@J45,@J110,@J111,@J112,@J113,@J114,@J115,@J116,"C2-BASE-AVAILABLE-knownzero","C2-BASE-REQUEST-none","C2-BASE-REQUEST-bool","C2-BASE-REQUEST-schema","C2-BASE-REQUEST-missing","C2-BASE-REQUEST-eventbool","C2-BASE-REQUEST-eventfloat","C2-BASE-REQUEST-eventzero","C2-BASE-APPLY-after-full",@J117,"C2-BASE-COST-not-applicable",@J118,@J60,"C2-BASE-RECOVER-no-receipt",@J63,@J73,@J70,@J74,@J75,@J78,@J81,"C2-bool-policy","C2-batch-null","C2-batch-empty","C2-batch-bool","C2-history-empty","C2-snapshot-payload","C2-receipt-digest","C2-receipt-equation","C2-planned-purpose","C2-planned-intent","C2-ledger-allocationEvent","C2-ledger-PolicyVersion",@J84,"C2-receipt-clause-principal","C2-receipt-clause-core","C2-chain","C2-recovery-scope","C2-JSON-control","C2-JSON-duplicate","C2-JSON-reverse","C2-JSON-same","C2-JSON-nested","C2-JSON-nan","C2-JSON-infinity","C2-JSON-counter","C2-ID-uid-min","C2-ID-uid-max","C2-ID-uid-true","C2-ID-uid-false","C2-ID-uid-zero","C2-ID-uid-float","C2-ID-uid-text","C2-ID-uid-overflow","C2-ID-account-min","C2-ID-account-max","C2-ID-account-true","C2-ID-account-false","C2-ID-account-zero","C2-ID-account-float","C2-ID-account-text","C2-ID-account-overflow","C2-ID-magic-min","C2-ID-magic-max","C2-ID-magic-true","C2-ID-magic-false","C2-ID-magic-zero","C2-ID-magic-float","C2-ID-magic-text","C2-ID-magic-overflow","C2-cost-bool-direct","C2-cost-unknown-field","C2-schema-unknown-field",@J90],"SchemaProbeSpecDigest":"a47011a94b7a2976047ddc3f293f31e0775444d617893eb064e055a4635f8432","SourcePins":{"Tests/Reference/hsbi_02b_r0d_independent_oracle.py":"ab3546751d8959058c0d8ea3965d08dd4345e1217f0c1a0d517ca34b554690c4","Tests/Reference/hsbi_02b_r0e_c2_contract_model.py":"cea97047d647ef44ee09d5942f4d16759460fe181b666244e932e263a0d6b223","Tests/Reference/hsbi_02b_r0e_c2_evidence.py":"5c8f2f7f24aa308c1bdeefe75831425898054d7f669e9afb12d0df5fb0c67330","Tests/Reference/hsbi_02b_r0e_c2_schemas.py":"ac97132f77772ce65cb991a64cf7280ab9ba3fe888446c9952513d31252588f6","Tests/Static/build_hsbi_02b_r0e_c2_catalog.py":"6095d765bd544967a697b4d06c2be00ac56e01cd91aa4b65cdf82ec898cd20e9","Tests/Static/check_hsbi_02b_r0d_contracts.py":"299ad1fe55ec79341488a87104f6f6999452c78d33b8e780d592ca7a8da881f8","Tests/Static/check_hsbi_02b_r0e_c1_contracts.py":"005723bb29afc3617237708c87e8b992346e785d064837e99c9210b00648dffb","Tests/Static/check_hsbi_02b_r0e_c2_contracts.py":"49c535477a6e503baa4e541bd083d0f9fdf8c73b608fdaee6b416ce16d8556a5","Tests/Static/check_hsbi_02b_r0e_c2_mutations.py":"4c50ac653c5e09acef468ce5f45860a8937e2bb9c282fca948cf2d5637cbd885"},"Tests":[@T5(["Positive"],"COMPOSITION",@T4(true,@J119,"COMMITTED_IN_MEMORY",false),"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-APPLY-positive","cases"),@T5(["Positive"],"SOURCE",2,"fund",@J120,@J91,"fund",121,@J121,"C2-BASE-SOURCE-positive","cases"),@T5(["Negative"],"SOURCE-RAW",@J122,"fund",@J120,@J91,"fund",121,@J121,"C2-BASE-SOURCE-raw","cases"),@T5(["Negative"],"SOURCE-NAMESPACE",@J122,"fund",@J120,@J91,"fund",121,@J121,"C2-BASE-SOURCE-namespace","cases"),@T5(["Negative"],"SOURCE-GRID",@J122,"fund",@J120,@J91,"fund",121,@J121,"C2-BASE-SOURCE-grid","cases"),@T5(["Negative"],"SOURCE-GRID","REJECT","economic_record",@J120,@J91,"economic_record",45,@J121,"C2-BASE-RECORD-grid","cases"),@T5(["Positive"],"BALANCE",true,"balance",@J120,@J91,"balance",61,@J121,"C2-BASE-BALANCE-control","cases"),@T5(["Negative"],"BALANCE",false,"balance",@J120,@J91,"balance",61,@J121,"C2-BASE-BALANCE-doublecount","cases"),@T5(["Negative","Composition"],"JOURNAL",@J124,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-APPLY-no-journal","cases"),@T5(["Positive"],"JOURNAL",["KNOWN_MODEL_AVAILABLE",["NUMBER","50","1"]],"available",@J120,@J91,"available",508,@J121,"C2-BASE-AVAILABLE-control","cases"),@T5(["Negative"],"JOURNAL",["UNAVAILABLE",null],"available",@J120,@J91,"available",508,@J121,@J98,"cases"),@T5(["Negative","Composition"],"COMPOSITION",@J124,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J99,"cases"),@T5(["Negative","Composition"],"ALLOCATION-VECTOR",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J55,"cases"),@T5(["Positive"],"IDENTITY","PASS","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,"C2-BASE-IDENTITY-control","cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J8,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J9,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J11,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J12,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J13,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J14,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J16,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J17,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J18,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J19,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J22,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J25,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J28,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J31,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J34,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J35,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J37,"cases"),@T5(@J126,"IDENTITY","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J39,"cases"),@T5(["Negative"],"ALLOCATION-EVENT","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J100,"cases"),@T5(["Negative"],"MALFORMED","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J66,"cases"),@T5(["Negative"],"MALFORMED","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J101,"cases"),@T5(["Negative"],"MALFORMED","REJECT","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,@J102,"cases"),@T5(["Negative"],"SNAPSHOT","UNAVAILABLE","verify_allocation_identity",@J120,@J91,"verify_allocation_identity",346,@J121,"C2-BASE-IDENTITY-stale","cases"),@T5(["Positive"],"BATCH",{"loss":["NUMBER","10","1"],"scope":"BATCH_MEMBERSHIP_VERIFIED_FIXTURE","status":"CONFIRMED","volume":["NUMBER","1","1"]},"assess_batch",@J120,@J91,"assess_batch",371,@J121,"C2-BASE-BATCH-control","cases"),@T5(["Negative"],"BATCH-NAMESPACE",{"status":"CONFLICT"},"assess_batch",@J120,@J91,"assess_batch",371,@J121,@J40,"cases"),@T5(["Negative"],"BATCH-LINEAGE",{"status":"CONFLICT"},"assess_batch",@J120,@J91,"assess_batch",371,@J121,@J103,"cases"),@T5(["Negative"],"BATCH-LINEAGE",{"status":"CONFLICT"},"assess_batch",@J120,@J91,"assess_batch",371,@J121,@J104,"cases"),@T5(["Negative"],"BATCH-LINEAGE",{"status":"CONFLICT"},"assess_batch",@J120,@J91,"assess_batch",371,@J121,"C2-BASE-BATCH-foreign-Cycle","cases"),@T5(["Negative"],"BATCH-LINEAGE",{"status":"CONFLICT"},"assess_batch",@J120,@J91,"assess_batch",371,@J121,"C2-BASE-BATCH-foreign-Order","cases"),@T5(["Negative"],"BATCH-LINEAGE",{"status":"CONFLICT"},"assess_batch",@J120,@J91,"assess_batch",371,@J121,@J105,"cases"),@T5(["Negative"],"BATCH-LINEAGE",{"status":"CONFLICT"},"assess_batch",@J120,@J91,"assess_batch",371,@J121,@J106,"cases"),@T5(["Negative"],"BATCH-LINEAGE",{"status":"CONFLICT"},"assess_batch",@J120,@J91,"assess_batch",371,@J121,@J107,"cases"),@T5(["Boundary"],"BATCH-COMPLETE",{"loss":["NUMBER","5","1"],"status":"PENDING","volume":["NUMBER","2","5"]},"assess_batch",@J120,@J91,"assess_batch",371,@J121,"C2-BASE-BATCH-pending","cases"),@T5(["Negative"],"BATCH-CAP",{"loss":["NUMBER","15","1"],"status":"OVER_CAP","volume":["NUMBER","1","1"]},"assess_batch",@J120,@J91,"assess_batch",371,@J121,"C2-BASE-BATCH-overcap","cases"),@T5(["Negative"],"BATCH",{"status":"UNAVAILABLE"},"assess_batch",@J120,@J91,"assess_batch",371,@J121,@J57,"cases"),@T5(["Positive"],"COST",{"AdditionalRisk":["NUMBER","1","2"],"scope":@J127,"status":"COVERED"},"cost_coverage",@J120,@J91,"cost_coverage",406,@J121,"C2-BASE-COST-control","cases"),@T5(["Negative"],"COST-INVENTORY",{"status":"CONFLICT"},"cost_coverage",@J120,@J91,"cost_coverage",406,@J121,"C2-BASE-COST-missing","cases"),@T5(["Negative"],"COST-ONCE",{"status":"CONFLICT"},"cost_coverage",@J120,@J91,"cost_coverage",406,@J121,"C2-BASE-COST-omitted","cases"),@T5(["Negative"],"COST",{"status":"UNAVAILABLE"},"cost_coverage",@J120,@J91,"cost_coverage",406,@J121,"C2-BASE-COST-unknown","cases"),@T5(["Negative"],"COST-INVENTORY",{"status":"CONFLICT"},"cost_coverage",@J120,@J91,"cost_coverage",406,@J121,"C2-BASE-COST-duplicate","cases"),@T5(["Boundary"],"COST",@J128,"cost_coverage",@J120,@J91,"cost_coverage",406,@J121,"C2-BASE-COST-knownzero","cases"),@T5(["Positive"],"COST",@J128,"cost_coverage",@J120,@J91,"cost_coverage",406,@J121,"C2-BASE-COST-knownempty","cases"),@T5(["Negative","Composition"],"COMPOSITION-BATCH",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-APPLY-bypass-batch","cases"),@T5(["Negative","Composition"],"COMPOSITION-COST",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-APPLY-bypass-cost","cases"),@T5(["Negative","Composition"],"COMPOSITION-IDENTITY",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J54,"cases"),@T5(["Negative","Composition"],"COMPOSITION-PLANNED",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J49,"cases"),@T5(["Negative"],"POSITIVE-AMOUNT",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J108,"cases"),@T5(["Negative"],"COST-HEADROOM",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J61,"cases"),@T5(["Boundary","Conservation"],"COMPOSITION",@T4(true,@T3(["NUMBER","50","1"],["NUMBER","0","1"],1,["NUMBER","0","1"],3),"COMMITTED_IN_MEMORY",false),"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-APPLY-full","cases"),@T5(["Replay"],"REPLAY",@J129,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-REPLAY-exact","cases"),@T5(["Replay"],"REPLAY",@J130,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-REPLAY-changed","cases"),@T5(["Replay"],"REPLAY",@J130,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-REPLAY-authority","cases"),@T5(["Replay"],"REPLAY",@J129,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J109,"cases"),@T5(["Positive"],"RECOVERY","RECONCILED_MODEL_ONLY","recover_store",@J120,@J91,"recover_store",599,@J121,"C2-BASE-RECOVER-control","cases"),@T5(["Negative"],"RECOVERY","UNAVAILABLE","recover_store",@J120,@J91,"recover_store",599,@J121,"C2-BASE-RECOVER-forged","cases"),@T5(["Positive"],"BALANCE",true,"balance",@J120,@J91,"balance",61,@J121,"C2-BASE-BALANCE-no-reserve","cases"),@T5(["Negative"],"SOURCE-CAP",@J122,"fund",@J120,@J91,"fund",121,@J121,"C2-BASE-SOURCE-overfund","cases"),@T5(["Negative"],"SOURCE-SMALL","REJECT","fund",@J120,@J91,"fund",121,@J121,"C2-BASE-SOURCE-small","cases"),@T5(["Negative"],"SOURCE-PROJECTED","REJECT","fund",@J120,@J91,"fund",121,@J121,"C2-BASE-SOURCE-projected","cases"),@T5(["Positive"],"FUND-REPLAY",{"status":"NO_OP","zeroDelta":true},"fund",@J120,@J91,"fund",121,@J121,"C2-BASE-FUND-exact","cases"),@T5(["Negative"],"FUND-REPLAY",@J131,"fund",@J120,@J91,"fund",121,@J121,"C2-BASE-FUND-changed","cases"),@T5(["Negative"],"REPLAY-AUTHORITY",@J131,"fund",@J120,@J91,"fund",121,@J121,@J7,"cases"),@T5(["Negative"],"JOURNAL",["UNAVAILABLE",null],"available",@J120,@J91,"available",508,@J121,@J45,"cases"),@T5(["Negative","Composition"],"AUTHORITY",@J124,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J110,"cases"),@T5(["Negative","Composition"],"AUTHORITY",@J124,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J111,"cases"),@T5(["Negative","Composition"],"AUTHORITY",@J124,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J112,"cases"),@T5(["Negative","Composition"],"AUTHORITY",@J124,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J113,"cases"),@T5(["Negative","Composition"],"AUTHORITY",@J124,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J114,"cases"),@T5(["Negative","Composition"],"AUTHORITY",@J124,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J115,"cases"),@T5(["Negative","Composition"],"AUTHORITY",@J124,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J116,"cases"),@T5(["Positive"],"JOURNAL",["KNOWN_MODEL_AVAILABLE",["NUMBER","0","1"]],"available",@J120,@J91,"available",508,@J121,"C2-BASE-AVAILABLE-knownzero","cases"),@T5(["Negative"],"MALFORMED",@J122,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-REQUEST-none","cases"),@T5(["Negative"],"MALFORMED",@J122,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-REQUEST-bool","cases"),@T5(["Negative"],"MALFORMED",{"status":"UNAVAILABLE","zeroDelta":true},"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-REQUEST-schema","cases"),@T5(["Negative"],"MALFORMED",@J122,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-REQUEST-missing","cases"),@T5(["Negative"],"MALFORMED",@J122,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-REQUEST-eventbool","cases"),@T5(["Negative"],"MALFORMED",@J122,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-REQUEST-eventfloat","cases"),@T5(["Negative"],"MALFORMED",@J122,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-REQUEST-eventzero","cases"),@T5(["Negative","Conservation"],"COMPOSITION",@J122,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,"C2-BASE-APPLY-after-full","cases"),@T5(["Negative","Composition"],"COMPOSITION",@J122,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J117,"cases"),@T5(["Positive"],"COST",@J128,"cost_coverage",@J120,@J91,"cost_coverage",406,@J121,"C2-BASE-COST-not-applicable","cases"),@T5(["Negative"],"BATCH",{"status":"UNAVAILABLE"},"assess_batch",@J120,@J91,"assess_batch",371,@J121,@J118,"cases"),@T5(["Negative"],"COST",{"status":"UNAVAILABLE"},"cost_coverage",@J120,@J91,"cost_coverage",406,@J121,@J60,"cases"),@T5(["Negative"],"RECEIPTS","CONFLICT","recover_store",@J120,@J91,"recover_store",599,@J121,"C2-BASE-RECOVER-no-receipt","cases"),@T5(["Negative"],"RECEIPTS","CONFLICT","recover_store",@J120,@J91,"recover_store",599,@J121,@J63,"cases"),@T5(["Negative"],"HISTORICAL-RECEIPT","CONFLICT","recover_store",@J120,@J91,"recover_store",599,@J121,@J73,"cases"),@T5(["Negative"],"HISTORICAL-RECEIPT","CONFLICT","recover_store",@J120,@J91,"recover_store",599,@J121,@J70,"cases"),@T5(["Negative"],"HISTORICAL-RECEIPT","CONFLICT","recover_store",@J120,@J91,"recover_store",599,@J121,@J74,"cases"),@T5(["Negative"],"DIGEST-FORMAT","CONFLICT","recover_store",@J120,@J91,"recover_store",599,@J121,@J75,"cases"),@T5(["Negative"],"MALFORMED-JOURNAL",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J78,"cases"),@T5(["Negative"],"MALFORMED-STORE",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J121,@J81,"cases"),@T5(["C2"],"bool-policy",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J132,"C2-bool-policy","cases"),@T5(["C2"],"batch-null",@J124,"apply_for_test",@J120,@J91,"apply_for_test",583,@J132,"C2-batch-null","cases"),@T5(["C2"],"batch-empty",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J132,"C2-batch-empty","cases"),@T5(["C2"],"batch-bool",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J132,"C2-batch-bool","cases"),@T5(["C2"],"history-empty",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J132,"C2-history-empty","cases"),@T5(["C2"],"snapshot-payload","CONFLICT","recover_store",@J120,@J91,"recover_store",599,@J132,"C2-snapshot-payload","cases"),@T5(["C2"],"receipt-digest",@J133,"recover_store",@J120,@J91,"recover_store",599,@J132,"C2-receipt-digest","cases"),@T5(["C2"],"receipt-equation",@J133,"recover_store",@J120,@J91,"recover_store",599,@J132,"C2-receipt-equation","cases"),@T5(["C2"],"planned-purpose",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J132,"C2-planned-purpose","cases"),@T5(["C2"],"planned-intent",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J132,"C2-planned-intent","cases"),@T5(["C2"],"ledger-allocationEvent",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J132,"C2-ledger-allocationEvent","cases"),@T5(["C2"],"ledger-PolicyVersion",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J132,"C2-ledger-PolicyVersion","cases"),@T5(["C2"],"receipt-clause-nonnegative",@J133,"recover_store",@J120,@J91,"recover_store",599,@J132,@J84,"cases"),@T5(["C2"],"receipt-clause-principal",@J133,"recover_store",@J120,@J91,"recover_store",599,@J132,"C2-receipt-clause-principal","cases"),@T5(["C2"],"receipt-clause-core",@J133,"recover_store",@J120,@J91,"recover_store",599,@J132,"C2-receipt-clause-core","cases"),@T5(["C2"],"chain",{"consumed":[["NUMBER","20","1"],["NUMBER","50","1"]],"free":[["NUMBER","30","1"],["NUMBER","0","1"]],"initialFree":["NUMBER","50","1"],"statuses":["COMMITTED_IN_MEMORY","COMMITTED_IN_MEMORY","NO_OP","REJECT"],"zeroDeltaAfterFull":true},"apply_for_test",@J120,@J91,"apply_for_test",583,@J132,"C2-chain","cases"),@T5(["C2"],"recovery-scope",{"inputsUnchanged":true,"newAuthorization":"REJECT","recovery":"RECONCILED_MODEL_ONLY"},"recover_store",@J120,@J91,"recover_store",599,@J132,"C2-recovery-scope","cases"),@T5(["C2"],"JSON-control","VALID","loads",@J120,@J97,"loads",22,@J132,"C2-JSON-control","cases"),@T5(["C2"],"JSON-duplicate","REJECT","loads",@J120,@J97,"loads",22,@J132,"C2-JSON-duplicate","cases"),@T5(["C2"],"JSON-reverse","REJECT","loads",@J120,@J97,"loads",22,@J132,"C2-JSON-reverse","cases"),@T5(["C2"],"JSON-same","REJECT","loads",@J120,@J97,"loads",22,@J132,"C2-JSON-same","cases"),@T5(["C2"],"JSON-nested","REJECT","loads",@J120,@J97,"loads",22,@J132,"C2-JSON-nested","cases"),@T5(["C2"],"JSON-nan","REJECT","loads",@J120,@J97,"loads",22,@J132,"C2-JSON-nan","cases"),@T5(["C2"],"JSON-infinity","REJECT","loads",@J120,@J97,"loads",22,@J132,"C2-JSON-infinity","cases"),@T5(["C2"],"JSON-counter","REJECT","loads",@J120,@J97,"loads",22,@J132,"C2-JSON-counter","cases"),@T5(["C2"],"ID-uid-min","VALID","validate",@J120,@J96,"validate",45,@J132,"C2-ID-uid-min","cases"),@T5(["C2"],"ID-uid-max","VALID","validate",@J120,@J96,"validate",45,@J132,"C2-ID-uid-max","cases"),@T5(["C2"],"ID-uid-true","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-uid-true","cases"),@T5(["C2"],"ID-uid-false","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-uid-false","cases"),@T5(["C2"],"ID-uid-zero","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-uid-zero","cases"),@T5(["C2"],"ID-uid-float","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-uid-float","cases"),@T5(["C2"],"ID-uid-text","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-uid-text","cases"),@T5(["C2"],"ID-uid-overflow","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-uid-overflow","cases"),@T5(["C2"],"ID-account-min","VALID","validate",@J120,@J96,"validate",45,@J132,"C2-ID-account-min","cases"),@T5(["C2"],"ID-account-max","VALID","validate",@J120,@J96,"validate",45,@J132,"C2-ID-account-max","cases"),@T5(["C2"],"ID-account-true","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-account-true","cases"),@T5(["C2"],"ID-account-false","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-account-false","cases"),@T5(["C2"],"ID-account-zero","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-account-zero","cases"),@T5(["C2"],"ID-account-float","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-account-float","cases"),@T5(["C2"],"ID-account-text","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-account-text","cases"),@T5(["C2"],"ID-account-overflow","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-account-overflow","cases"),@T5(["C2"],"ID-magic-min","VALID","validate",@J120,@J96,"validate",45,@J132,"C2-ID-magic-min","cases"),@T5(["C2"],"ID-magic-max","VALID","validate",@J120,@J96,"validate",45,@J132,"C2-ID-magic-max","cases"),@T5(["C2"],"ID-magic-true","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-magic-true","cases"),@T5(["C2"],"ID-magic-false","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-magic-false","cases"),@T5(["C2"],"ID-magic-zero","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-magic-zero","cases"),@T5(["C2"],"ID-magic-float","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-magic-float","cases"),@T5(["C2"],"ID-magic-text","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-magic-text","cases"),@T5(["C2"],"ID-magic-overflow","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-ID-magic-overflow","cases"),@T5(["C2"],"cost-bool-direct","CONFLICT","cost_coverage",@J120,@J91,"cost_coverage",406,@J132,"C2-cost-bool-direct","cases"),@T5(["C2"],"cost-unknown-field","CONFLICT","cost_coverage",@J120,@J91,"cost_coverage",406,@J132,"C2-cost-unknown-field","cases"),@T5(["C2"],"schema-unknown-field","REJECT","validate",@J120,@J96,"validate",45,@J132,"C2-schema-unknown-field","cases"),@T5(["C2"],"authority-unused-malformed",@J125,"apply_for_test",@J120,@J91,"apply_for_test",583,@J132,@J90,"cases")]}
@T1=OBJECT_KEYS["ClauseID","ContractID","ExpectedScope","GuardID","MutationID","NegativeTestID","PositiveTestID","RedundancyProof","SubjectFunction"]
@T2=OBJECT_KEYS["ExactEdit","ExpectedVerdict","GuardID","MutationID","NegativeTestID","PositiveTestID","RedundancyProof","TargetFile","TargetFunction"]
@T3=OBJECT_KEYS["consumed","free","receipts","reserved","revision"]
@T4=OBJECT_KEYS["inputsUnchanged","state","status","zeroDelta"]
@T5=OBJECT_KEYS["Classes","GuardGroup","IndependentExpected","Operation","ProofBoundary","SourceFile","SourceFunction","SourceLine","TestFile","TestID","TestImplementation"]
@J1="causal public API or mathematical schema helper"
@J2="C2-C1-GUARD-source-namespace"
@J3="C2-C1-GUARD-balance-reserved"
@J4="C2-C1-GUARD-projected-source"
@J5="C2-C1-MUT-fund-immutable-before-replay"
@J6="C2-C1-GUARD-fund-immutable-before-replay"
@J7="C2-BASE-FUND-authority-change"
@J8="C2-BASE-IDENTITY-foreign-Broker"
@J9="C2-BASE-IDENTITY-foreign-Server"
@J10="C2-C1-GUARD-identity-Account"
@J11="C2-BASE-IDENTITY-foreign-Account"
@J12="C2-BASE-IDENTITY-foreign-Symbol"
@J13="C2-BASE-IDENTITY-foreign-Magic"
@J14="C2-BASE-IDENTITY-foreign-Cycle"
@J15="C2-C1-GUARD-identity-Position"
@J16="C2-BASE-IDENTITY-foreign-Position"
@J17="C2-BASE-IDENTITY-foreign-Deal"
@J18="C2-BASE-IDENTITY-foreign-Order"
@J19="C2-BASE-IDENTITY-foreign-Role"
@J20="C2-C1-MUT-identity-EconomicEventID"
@J21="C2-C1-GUARD-identity-EconomicEventID"
@J22="C2-BASE-IDENTITY-foreign-EconomicEventID"
@J23="C2-C1-MUT-identity-AllocationEventID"
@J24="C2-C1-GUARD-identity-AllocationEventID"
@J25="C2-BASE-IDENTITY-foreign-AllocationEventID"
@J26="C2-C1-MUT-identity-ConsumptionEventID"
@J27="C2-C1-GUARD-identity-ConsumptionEventID"
@J28="C2-BASE-IDENTITY-foreign-ConsumptionEventID"
@J29="C2-C1-MUT-identity-AllocationID"
@J30="C2-C1-GUARD-identity-AllocationID"
@J31="C2-BASE-IDENTITY-foreign-AllocationID"
@J32="C2-C1-MUT-identity-PolicyVersion"
@J33="C2-C1-GUARD-identity-PolicyVersion"
@J34="C2-BASE-IDENTITY-foreign-PolicyVersion"
@J35="C2-BASE-IDENTITY-foreign-Plan"
@J36="C2-C1-GUARD-identity-Revision"
@J37="C2-BASE-IDENTITY-foreign-Revision"
@J38="C2-C1-GUARD-identity-Snapshot"
@J39="C2-BASE-IDENTITY-foreign-Snapshot"
@J40="C2-BASE-BATCH-foreign-account"
@J41="C2-C1-MUT-batch-completeness"
@J42="C2-C1-GUARD-batch-completeness"
@J43="C2-C1-MUT-available-journal-layer"
@J44="C2-C1-GUARD-available-journal-layer"
@J45="C2-BASE-AVAILABLE-external-missing"
@J46="C2-C1-GUARD-composition-batch"
@J47="C2-C1-GUARD-composition-cost"
@J48="C2-C1-GUARD-planned-operation"
@J49="C2-BASE-APPLY-bypass-planned"
@J50="C2-C1-MUT-immutable-before-replay"
@J51="C2-C1-GUARD-immutable-before-replay"
@J52="C2-C1-MUT-apply-revalidation"
@J53="C2-C1-GUARD-apply-revalidation"
@J54="C2-BASE-APPLY-bypass-identity"
@J55="C2-BASE-APPLY-forged-allocation"
@J56="Public apply always authorizes: _reconcile_store reconstructs ALL pre-state rows from independent journal. _operate_for_registry_replay calls _apply_registry_delta, which validates selected row before and after exact delta and returns no commit on failure. apply checks returned status. Other rows unchanged. Thus outer repeat is redundant over the declared public input domain; mutation of mandatory private delta itself is outside this equivalence claim."
@J57="C2-BASE-BATCH-unknown-policy"
@J58="C2-C1-MUT-cost-provider-complete"
@J59="C2-C1-GUARD-cost-provider-complete"
@J60="C2-BASE-COST-provider-incomplete"
@J61="C2-BASE-APPLY-insufficient-headroom"
@J62="C2-C1-GUARD-receipt-inventory"
@J63="C2-BASE-RECOVER-bad-source-digest"
@J64="C2-C1-MUT-malformed-default-identity"
@J65="C2-C1-GUARD-malformed-default-identity"
@J66="C2-BASE-IDENTITY-malformed-none"
@J67="C2 public authorize/_reconcile_store/verify_allocation_identity validates nested schema before this old clause. Mandatory schema cannot be bypassed by public apply. Original and mutant preserve the typed rejection on this causal input; not an unsafe acceptance kill."
@J68="C2-C1-MUT-historical-allocation"
@J69="C2-C1-GUARD-historical-allocation"
@J70="C2-BASE-RECOVER-historical-allocation"
@J71="C2-C1-MUT-historical-identity"
@J72="C2-C1-GUARD-historical-identity"
@J73="C2-BASE-RECOVER-historical-identity"
@J74="C2-BASE-RECOVER-historical-plan"
@J75="C2-BASE-RECOVER-digest-format"
@J76="C2-C1-MUT-journal-self-repair"
@J77="C2-C1-GUARD-journal-self-repair"
@J78="C2-BASE-APPLY-bad-journal-entry"
@J79="C2-C1-MUT-malformed-source-ignore"
@J80="C2-C1-GUARD-malformed-source-ignore"
@J81="C2-BASE-APPLY-bad-store-source"
@J82="C2-MUT-receipt-risk-nonnegative"
@J83="C2-GUARD-receipt-risk-nonnegative"
@J84="C2-receipt-clause-nonnegative"
@J85="Mandatory CostClaim schema rejects the boolean claim before fact comparison; removing only the CostSet caller cannot bypass it. Direct cost_coverage and public apply both preserve rejection. Dual caller mutation separately demonstrates necessity of the complete layer."
@J86="C2-MUT-cost-dual-shape-callers"
@J87="C2-GUARD-cost-dual-shape-callers"
@J88="C2-MUT-mandatory-authority-caller"
@J89="C2-GUARD-mandatory-authority-caller"
@J90="C2-authority-unused-malformed"
@J91="Tests/Reference/hsbi_02b_r0e_c2_contract_model.py"
@J92="for k in expected) else 'REJECT'  # GUARD:C1-IDENTITY"
@J93="for k in ('bucket','purpose','intent')"
@J94="if expected is not None:dto.validate(\"CostSet\",expected)"
@J95={"new":"pass","old":@J94}
@J96="Tests/Reference/hsbi_02b_r0e_c2_schemas.py"
@J97="Tests/Reference/hsbi_02b_r0e_c2_evidence.py"
@J98="C2-BASE-AVAILABLE-incomplete"
@J99="C2-BASE-APPLY-missing-authority"
@J100="C2-BASE-IDENTITY-allocation-event"
@J101="C2-BASE-IDENTITY-malformed-bool"
@J102="C2-BASE-IDENTITY-malformed-missing"
@J103="C2-BASE-BATCH-foreign-BatchID"
@J104="C2-BASE-BATCH-foreign-Symbol"
@J105="C2-BASE-BATCH-foreign-Position"
@J106="C2-BASE-BATCH-foreign-currency"
@J107="C2-BASE-BATCH-foreign-digits"
@J108="C2-BASE-APPLY-negative-amount"
@J109="C2-BASE-REPLAY-current-context"
@J110="C2-BASE-APPLY-provider-missing-allocations"
@J111="C2-BASE-APPLY-provider-missing-context"
@J112="C2-BASE-APPLY-provider-missing-batches"
@J113="C2-BASE-APPLY-provider-missing-fillHistory"
@J114="C2-BASE-APPLY-provider-missing-costSets"
@J115="C2-BASE-APPLY-provider-missing-coreJournal"
@J116="C2-BASE-APPLY-provider-missing-receipts"
@J117="C2-BASE-APPLY-token-not-authority"
@J118="C2-BASE-BATCH-history-incomplete"
@J119=@T3(["NUMBER","10","1"],["NUMBER","40","1"],1,["NUMBER","0","1"],3)
@J120="C2 DTO/fixture composition; no broker/durable/global funding proof"
@J121="Tests/Static/check_hsbi_02b_r0e_c1_contracts.py"
@J122={"status":"REJECT","zeroDelta":true}
@J123=@T3(["NUMBER","0","1"],["NUMBER","50","1"],0,["NUMBER","0","1"],2)
@J124=@T4(true,@J123,"UNAVAILABLE",true)
@J125=@T4(true,@J123,"REJECT",true)
@J126=["Negative","Identity conflict"]
@J127="COMPLETE_APPLICABLE_FIXTURE_COSTSET"
@J128={"AdditionalRisk":["NUMBER","0","1"],"scope":@J127,"status":"COVERED"}
@J129={"state":@J119,"status":"NO_OP","zeroDelta":true}
@J130={"state":@J119,"status":"CONFLICT","zeroDelta":true}
@J131={"status":"CONFLICT","zeroDelta":true}
@J132="Tests/Static/check_hsbi_02b_r0e_c2_contracts.py"
@J133={"inputsUnchanged":true,"status":"CONFLICT"}
```

## R3 — точные межфайловые ссылки mutation catalogs

R1/R2 прочитаны целиком. Для R3..R7 ниже сохранены exact raw-token unchanged record ordinals предыдущего файла и все изменения полей/additions с восстановлением полного token stream. Это статическое чтение каталогов, не применение или выполнение mutations. Whole-file duplicates этим методом не добавляются.

### Mutation catalog R3

````text
FILE Tests/Static/hsb_2d_v1_r3_mutations.json SHA256 feb4cbc316c307a09c85ec6ab4c7092f9e6337000508d973b1f8ed4498509363
BASE Tests/Static/hsb_2d_v1_r2_mutations.json SHA256 b12d49d18bf4f69ebd811cf4ba96836cfc33ca73ce7ab2ca74c63dd67fa01c0b
Exact unchanged record ordinals [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 48, 49, 50, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 67, 68, 69, 72, 73, 74, 77, 78, 79, 82, 83, 84, 87, 88, 89, 92, 93, 94, 97, 98, 99]
39 PATCH remove=[] set={"expected_check_ids":["S040A"],"old":"REAL_TRADING_ALLOWED=NO\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->"}
40 PATCH remove=[] set={"expected_check_ids":["S040A"]}
41 PATCH remove=[] set={"expected_check_ids":["S040A"]}
42 PATCH remove=[] set={"expected_check_ids":["S040A"]}
43 PATCH remove=[] set={"expected_check_ids":["S040A"]}
44 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R3_CANONICAL_STATUS_BEGIN -->"}
51 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R3_FILE_MANIFEST_SHA256.txt"}
52 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R3_FILE_MANIFEST_SHA256.txt"}
53 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R3_FILE_MANIFEST_SHA256.txt"}
54 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R3_FILE_MANIFEST_SHA256.txt"}
55 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R3_FILE_MANIFEST_SHA256.txt"}
66 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->"}
70 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R3_CANONICAL_STATUS_BEGIN -->"}
71 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->"}
75 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R3_CANONICAL_STATUS_BEGIN -->"}
76 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->"}
80 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R3_CANONICAL_STATUS_BEGIN -->"}
81 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->"}
85 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R3_CANONICAL_STATUS_BEGIN -->"}
86 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->"}
90 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R3_CANONICAL_STATUS_BEGIN -->"}
91 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->"}
95 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R3_CANONICAL_STATUS_BEGIN -->"}
96 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\n```\n<!-- HSB_2D_V1_R3_CANONICAL_STATUS_END -->"}
100 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R3_CANONICAL_STATUS_BEGIN -->"}
101 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R3_CLEAN_RESULT.txt","mutation_type":"historical_superseded","required":false}
102 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R3_MUTATION_RESULTS.json","mutation_type":"historical_superseded","required":false}
103 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R3_EVIDENCE_SEAL_SHA256.txt","mutation_type":"historical_superseded","required":false}
104 ADD {"id":"M104","name":"STATE_REVISION_GUARD_INSIDE_IF_FALSE","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(false){if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");}"}
105 ADD {"id":"M105","name":"STATE_REVISION_GUARD_INSIDE_WHILE_FALSE","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"while(false){if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");}"}
106 ADD {"id":"M106","name":"STATE_REVISION_GUARD_INSIDE_FOR_FALSE","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"for(;false;){if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");}"}
107 ADD {"id":"M107","name":"STATE_REVISION_GUARD_AFTER_UNCONDITIONAL_RETURN","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"return HSBI_RuntimeReject(x,HSBI_DECISION_VALID,HSBI_RD_OK,\"EARLY\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
108 ADD {"id":"M108","name":"STATE_REVISION_GUARD_ONLY_INSIDE_RUNTIME_CONDITIONAL","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(x.marketFresh){if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");}"}
109 ADD {"id":"M109","name":"STATE_REVISION_GUARD_MOVED_TO_UNUSED_HELPER","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"void HSBI_UnusedMutation(){if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");}"}
110 ADD {"id":"M110","name":"BLOCK_COMMENT_CONTAINS_FAKE_PREPROCESSOR_ELSE","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"#if 0\n/*\n#else\n*/\nif(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");\n#endif"}
111 ADD {"id":"M111","name":"BLOCK_COMMENT_CONTAINS_FAKE_PREPROCESSOR_ELIF","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"#if 0\n/*\n#elif 1\n*/\nif(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");\n#endif"}
112 ADD {"id":"M112","name":"BLOCK_COMMENT_CONTAINS_FAKE_PREPROCESSOR_ENDIF","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"#if 0\n/*\n#endif\n*/\nif(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");\n#endif"}
113 ADD {"id":"M113","name":"STRING_CONTAINS_FAKE_PREPROCESSOR_DIRECTIVE","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"#if 0\nstring fake=\"#else\";\nif(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");\n#endif"}
114 ADD {"id":"M114","name":"STATUS_AND_REASON_TOKENS_SPLIT_ACROSS_UNRELATED_REJECTS","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_STATE_REVISION_MISMATCH,\"A\");if(x.planId==0)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_CONTEXT_INVALID,\"B\");"}
115 ADD {"id":"M115","name":"CORRECT_GUARD_WITH_WRONG_REJECT_ARGUMENT_ORDER","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_RD_STATE_REVISION_MISMATCH,HSBI_DECISION_CONFLICT,\"HSBI-2D-REV\");"}
116 ADD {"id":"M116","name":"tamper_clean","target":"Tests/Evidence/HSB_2D_V1_R3_CLEAN_RESULT.txt","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"RESULT=PASS","new":"RESULT=TAMPERED"}
117 ADD {"id":"M117","name":"tamper_json","target":"Tests/Evidence/HSB_2D_V1_R3_MUTATION_RESULTS.json","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"\"schema\": \"HSB.2D-V1-R1/mutations/1\"","new":"\"schema\": \"TAMPERED\""}
118 ADD {"id":"M118","name":"tamper_text","target":"Tests/Evidence/HSB_2D_V1_R3_MUTATION_RESULTS.txt","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"M001|TARGET=","new":"TAMPERED|TARGET="}
119 ADD {"id":"M119","name":"tamper_catalog","target":"Tests/Static/hsb_2d_v1_r3_mutations.json","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"\"name\": \"STATE_REVISION_GUARD_INSIDE_IF_FALSE\"","new":"\"name\": \"TAMPERED\""}
120 ADD {"id":"M120","name":"seal_remove","target":"Tests/Evidence/HSB_2D_V1_R3_EVIDENCE_SEAL_SHA256.txt","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"__SEAL_SPECIAL__","new":"seal_remove"}
121 ADD {"id":"M121","name":"seal_extra","target":"Tests/Evidence/HSB_2D_V1_R3_EVIDENCE_SEAL_SHA256.txt","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"__SEAL_SPECIAL__","new":"seal_extra"}
122 ADD {"id":"M122","name":"seal_duplicate","target":"Tests/Evidence/HSB_2D_V1_R3_EVIDENCE_SEAL_SHA256.txt","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"__SEAL_SPECIAL__","new":"seal_duplicate"}
123 ADD {"id":"M123","name":"seal_bad_hash","target":"Tests/Evidence/HSB_2D_V1_R3_EVIDENCE_SEAL_SHA256.txt","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"__SEAL_SPECIAL__","new":"seal_bad_hash"}
Removed trailing baseline records []
````

### Mutation catalog R4

````text
FILE Tests/Static/hsb_2d_v1_r4_mutations.json SHA256 cb3f8fef65299cee89c51f73761262993f34bbb4fe194577ec9814ceef0c21b1
BASE Tests/Static/hsb_2d_v1_r3_mutations.json SHA256 feb4cbc316c307a09c85ec6ab4c7092f9e6337000508d973b1f8ed4498509363
Exact unchanged record ordinals [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 67, 68, 69, 72, 73, 74, 77, 78, 79, 82, 83, 84, 87, 88, 89, 92, 93, 94, 97, 98, 99, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115]
39 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->"}
44 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R4_CANONICAL_STATUS_BEGIN","new":"<!-- marker removed"}
51 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R4_FILE_MANIFEST_SHA256.txt"}
52 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R4_FILE_MANIFEST_SHA256.txt"}
53 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R4_FILE_MANIFEST_SHA256.txt"}
54 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R4_FILE_MANIFEST_SHA256.txt"}
55 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R4_FILE_MANIFEST_SHA256.txt"}
66 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->"}
70 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R4_CANONICAL_STATUS_BEGIN","new":"<!-- marker removed"}
71 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->"}
75 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R4_CANONICAL_STATUS_BEGIN","new":"<!-- marker removed"}
76 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->"}
80 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R4_CANONICAL_STATUS_BEGIN","new":"<!-- marker removed"}
81 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->"}
85 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R4_CANONICAL_STATUS_BEGIN","new":"<!-- marker removed"}
86 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->"}
90 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R4_CANONICAL_STATUS_BEGIN","new":"<!-- marker removed"}
91 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->"}
95 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R4_CANONICAL_STATUS_BEGIN","new":"<!-- marker removed"}
96 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R4_CANONICAL_STATUS_END -->"}
100 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R4_CANONICAL_STATUS_BEGIN","new":"<!-- marker removed"}
101 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R4_CLEAN_RESULT.txt","mutation_type":"evidence","required":true}
102 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R4_MUTATION_RESULTS.json","mutation_type":"evidence","required":true}
103 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R4_EVIDENCE_SEAL_SHA256.txt","mutation_type":"evidence","required":true}
116 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R4_CLEAN_RESULT.txt"}
117 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R4_MUTATION_RESULTS.json","old":"\"schema\": \"HSB.2D-V1-R4/mutations/1\""}
118 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R4_MUTATION_RESULTS.txt"}
119 PATCH remove=[] set={"target":"Tests/Static/hsb_2d_v1_r4_mutations.json"}
120 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R4_EVIDENCE_SEAL_SHA256.txt"}
121 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R4_EVIDENCE_SEAL_SHA256.txt"}
122 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R4_EVIDENCE_SEAL_SHA256.txt"}
123 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R4_EVIDENCE_SEAL_SHA256.txt"}
124 ADD {"id":"M124","name":"CONDITIONAL_EARLY_VALID_RETURN_BEFORE_STATE_REVISION_GUARD","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(x.stateRevision!=revision){HSBI_RuntimeDecisionResult q=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,HSBI_RD_OK,\"BYPASS\");q.valid=true;return q;}if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
125 ADD {"id":"M125","name":"ONE_LINE_UNKNOWN_SUCCESS_BEFORE_REVISION","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(x.stateRevision!=revision)return HSBI_MakeValidRuntimeDecision(x);if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
126 ADD {"id":"M126","name":"SUCCESS_THROUGH_ELSE_BEFORE_REVISION","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(x.stateRevision==revision){}else{HSBI_RuntimeDecisionResult result;result.valid=true;return result;}if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
127 ADD {"id":"M127","name":"VALID_STATUS_BEFORE_REVISION","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"HSBI_RuntimeDecisionResult result;result.status=HSBI_DECISION_VALID;return result;if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
128 ADD {"id":"M128","name":"VALID_FLAG_BEFORE_REVISION","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"HSBI_RuntimeDecisionResult result;result.valid=true;return result;if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
129 ADD {"id":"M129","name":"UNKNOWN_HELPER_BEFORE_REVISION","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(x.stateRevision!=revision)return HSBI_UnknownDecisionHelper(x);if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
130 ADD {"id":"M130","name":"SUCCESS_BEFORE_PERSISTENCE","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S038"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(!x.persistencePrepared)return HSBI_RuntimeReject(x,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_RD_PERSISTENCE_REQUIRED,\"HSBI-2D-PERSIST\");","new":"if(!x.persistencePrepared){HSBI_RuntimeDecisionResult q=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,HSBI_RD_OK,\"BYPASS\");q.valid=true;return q;}if(!x.persistencePrepared)return HSBI_RuntimeReject(x,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_RD_PERSISTENCE_REQUIRED,\"HSBI-2D-PERSIST\");"}
131 ADD {"id":"M131","name":"SUCCESS_BEFORE_DIGEST","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S039D"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.inputDigest==\"\"||x.inputDigest!=HSBI_RuntimeDecisionContextDigest(x))return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_DIGEST_MISMATCH,\"HSBI-2D-DIGEST\");","new":"if(x.inputDigest==\"\"){HSBI_RuntimeDecisionResult q=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,HSBI_RD_OK,\"BYPASS\");q.valid=true;return q;}if(x.inputDigest==\"\"||x.inputDigest!=HSBI_RuntimeDecisionContextDigest(x))return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_DIGEST_MISMATCH,\"HSBI-2D-DIGEST\");"}
132 ADD {"id":"M132","name":"REJECT_CONSTRUCTOR_SETS_VALID","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["SREJECT"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"ZeroMemory(r);r.status=status;r.reason=reason;","new":"ZeroMemory(r);r.valid=true;r.status=status;r.reason=reason;"}
133 ADD {"id":"M133","name":"REJECT_CONSTRUCTOR_SUBSTITUTES_STATUS","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["SREJECT"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"ZeroMemory(r);r.status=status;r.reason=reason;","new":"ZeroMemory(r);r.status=HSBI_DECISION_VALID;r.reason=reason;"}
134 ADD {"id":"M134","name":"MULTIPLE_SUCCESS_PATHS","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(x.stateRevision!=revision){HSBI_RuntimeDecisionResult q=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,HSBI_RD_OK,\"BYPASS\");q.valid=true;return q;}if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
135 ADD {"id":"M135","name":"GUARD_AFTER_CONDITIONAL_SUCCESS","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(x.stateRevision!=revision){HSBI_RuntimeDecisionResult q=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,HSBI_RD_OK,\"BYPASS\");q.valid=true;return q;}if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
Removed trailing baseline records []
````

### Mutation catalog R5

````text
FILE Tests/Static/hsb_2d_v1_r5_mutations.json SHA256 683d19672baa21b602a11b6a156adb813268e0a6a811cd32264f36d347e8a513
BASE Tests/Static/hsb_2d_v1_r4_mutations.json SHA256 cb3f8fef65299cee89c51f73761262993f34bbb4fe194577ec9814ceef0c21b1
Exact unchanged record ordinals [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 67, 68, 69, 72, 73, 74, 77, 78, 79, 82, 83, 84, 87, 88, 89, 92, 93, 94, 97, 98, 99, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135]
39 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->"}
44 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R5_CANONICAL_STATUS_BEGIN"}
51 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R5_FILE_MANIFEST_SHA256.txt"}
52 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R5_FILE_MANIFEST_SHA256.txt"}
53 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R5_FILE_MANIFEST_SHA256.txt"}
54 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R5_FILE_MANIFEST_SHA256.txt"}
55 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R5_FILE_MANIFEST_SHA256.txt"}
66 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->"}
70 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R5_CANONICAL_STATUS_BEGIN"}
71 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->"}
75 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R5_CANONICAL_STATUS_BEGIN"}
76 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->"}
80 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R5_CANONICAL_STATUS_BEGIN"}
81 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->"}
85 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R5_CANONICAL_STATUS_BEGIN"}
86 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->"}
90 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R5_CANONICAL_STATUS_BEGIN"}
91 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->"}
95 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R5_CANONICAL_STATUS_BEGIN"}
96 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R5_CANONICAL_STATUS_END -->"}
100 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R5_CANONICAL_STATUS_BEGIN"}
101 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R5_CLEAN_RESULT.txt"}
102 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R5_MUTATION_RESULTS.json"}
103 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R5_EVIDENCE_SEAL_SHA256.txt"}
116 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R5_CLEAN_RESULT.txt"}
117 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R5_MUTATION_RESULTS.json","old":"\"schema\": \"HSB.2D-V1-R5/mutations/1\""}
118 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R5_MUTATION_RESULTS.txt"}
119 PATCH remove=[] set={"target":"Tests/Static/hsb_2d_v1_r5_mutations.json"}
120 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R5_EVIDENCE_SEAL_SHA256.txt"}
121 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R5_EVIDENCE_SEAL_SHA256.txt"}
122 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R5_EVIDENCE_SEAL_SHA256.txt"}
123 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R5_EVIDENCE_SEAL_SHA256.txt"}
136 ADD {"id":"M136","name":"ENUM_ZERO_COMPUTED_VALID_COMBINED","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028","SREJECT"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(revision!=x.stateRevision)return HSBI_RuntimeReject(x,(HSBI_RuntimeDecisionStatus)0,HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","replacements":[["ZeroMemory(r);r.status=status;r.reason=reason;","ZeroMemory(r);r.valid=(status==(HSBI_RuntimeDecisionStatus)0);r.status=status;r.reason=reason;"],["if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","if(revision!=x.stateRevision)return HSBI_RuntimeReject(x,(HSBI_RuntimeDecisionStatus)0,HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"]]}
137 ADD {"id":"M137","name":"NUMERIC_ENUM_STATUS","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(revision!=x.stateRevision)return HSBI_RuntimeReject(x,(HSBI_RuntimeDecisionStatus)0,HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
138 ADD {"id":"M138","name":"STATUS_VARIABLE_ALIAS","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"HSBI_RuntimeDecisionStatus statusAlias=(HSBI_RuntimeDecisionStatus)0;if(revision!=x.stateRevision)return HSBI_RuntimeReject(x,statusAlias,HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
139 ADD {"id":"M139","name":"VALID_BOOL_CAST","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["SREJECT"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"ZeroMemory(r);r.status=status;r.reason=reason;","new":"ZeroMemory(r);r.valid=(bool)1;r.status=status;r.reason=reason;"}
140 ADD {"id":"M140","name":"VALID_NUMERIC","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["SREJECT"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"ZeroMemory(r);r.status=status;r.reason=reason;","new":"ZeroMemory(r);r.valid=1;r.status=status;r.reason=reason;"}
141 ADD {"id":"M141","name":"VALID_NOT_FALSE","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["SREJECT"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"ZeroMemory(r);r.status=status;r.reason=reason;","new":"ZeroMemory(r);r.valid=!false;r.status=status;r.reason=reason;"}
142 ADD {"id":"M142","name":"VALID_FROM_STATUS","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["SREJECT"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"ZeroMemory(r);r.status=status;r.reason=reason;","new":"ZeroMemory(r);r.valid=(status==HSBI_DECISION_VALID);r.status=status;r.reason=reason;"}
143 ADD {"id":"M143","name":"NUMERIC_STATUS_OVERWRITE","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["SREJECT"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"ZeroMemory(r);r.status=status;r.reason=reason;","new":"ZeroMemory(r);r.status=(HSBI_RuntimeDecisionStatus)0;r.status=status;r.reason=reason;"}
144 ADD {"id":"M144","name":"REVERSED_REVISION_SUCCESS","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(revision!=x.stateRevision)return HSBI_RuntimeReject(x,HSBI_DECISION_VALID,HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
145 ADD {"id":"M145","name":"REVERSED_EQUALITY_BYPASS","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(revision==x.stateRevision){}else{return HSBI_RuntimeReject(x,HSBI_DECISION_VALID,HSBI_RD_OK,\"BYPASS\");}if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
146 ADD {"id":"M146","name":"LOCAL_CONST_STATUS_ALIAS","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"const HSBI_RuntimeDecisionStatus ok=(HSBI_RuntimeDecisionStatus)0;if(revision!=x.stateRevision)return HSBI_RuntimeReject(x,ok,HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
147 ADD {"id":"M147","name":"TERNARY_STATUS","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(revision!=x.stateRevision)return HSBI_RuntimeReject(x,x.immutable?HSBI_DECISION_REJECTED:HSBI_DECISION_VALID,HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
148 ADD {"id":"M148","name":"SECOND_STATUS_ASSIGNMENT","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["SREJECT"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"ZeroMemory(r);r.status=status;r.reason=reason;","new":"ZeroMemory(r);r.status=status;r.status=HSBI_DECISION_CONFLICT;r.reason=reason;"}
149 ADD {"id":"M149","name":"SECOND_REASON_ASSIGNMENT","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["SREJECT"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"ZeroMemory(r);r.status=status;r.reason=reason;","new":"ZeroMemory(r);r.status=status;r.reason=reason;r.reason=HSBI_RD_OK;"}
150 ADD {"id":"M150","name":"UNKNOWN_HELPER_STATUS","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(revision!=x.stateRevision)return HSBI_RuntimeReject(x,HSBI_GetDecisionStatus(),HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
Removed trailing baseline records []
````

### Mutation catalog R6

````text
FILE Tests/Static/hsb_2d_v1_r6_mutations.json SHA256 370ccb3e02bcbbdabc88b4bfa2a43aa59fd997a88d5e5bfc047b3994500b2051
BASE Tests/Static/hsb_2d_v1_r5_mutations.json SHA256 683d19672baa21b602a11b6a156adb813268e0a6a811cd32264f36d347e8a513
Exact unchanged record ordinals [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 67, 68, 69, 72, 73, 74, 77, 78, 79, 82, 83, 84, 87, 88, 89, 92, 93, 94, 97, 98, 99, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150]
39 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->"}
44 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R6_CANONICAL_STATUS_BEGIN"}
51 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R6_FILE_MANIFEST_SHA256.txt"}
52 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R6_FILE_MANIFEST_SHA256.txt"}
53 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R6_FILE_MANIFEST_SHA256.txt"}
54 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R6_FILE_MANIFEST_SHA256.txt"}
55 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R6_FILE_MANIFEST_SHA256.txt"}
66 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->"}
70 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R6_CANONICAL_STATUS_BEGIN"}
71 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->"}
75 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R6_CANONICAL_STATUS_BEGIN"}
76 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->"}
80 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R6_CANONICAL_STATUS_BEGIN"}
81 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->"}
85 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R6_CANONICAL_STATUS_BEGIN"}
86 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->"}
90 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R6_CANONICAL_STATUS_BEGIN"}
91 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->"}
95 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R6_CANONICAL_STATUS_BEGIN"}
96 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R6_CANONICAL_STATUS_END -->"}
100 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R6_CANONICAL_STATUS_BEGIN"}
101 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R6_CLEAN_RESULT.txt"}
102 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R6_MUTATION_RESULTS.json"}
103 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R6_EVIDENCE_SEAL_SHA256.txt"}
116 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R6_CLEAN_RESULT.txt"}
117 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R6_MUTATION_RESULTS.json","old":"\"schema\": \"HSB.2D-V1-R6/mutations/1\""}
118 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R6_MUTATION_RESULTS.txt"}
119 PATCH remove=[] set={"target":"Tests/Static/hsb_2d_v1_r6_mutations.json"}
120 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R6_EVIDENCE_SEAL_SHA256.txt"}
121 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R6_EVIDENCE_SEAL_SHA256.txt"}
122 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R6_EVIDENCE_SEAL_SHA256.txt"}
123 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R6_EVIDENCE_SEAL_SHA256.txt"}
151 ADD {"id":"M151","name":"NO_OP_REVISION_NEGATED","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(!(revision==x.stateRevision))return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
152 ADD {"id":"M152","name":"NO_OP_IDENTITY","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S026"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.accountLogin!=account||x.symbol!=symbol||x.magic!=magic||x.cycleId!=cycle||x.planId!=plan)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_IDENTITY_MISMATCH,\"HSBI-2D-ID\");","new":"if(x.accountLogin!=account||x.symbol!=symbol||x.magic!=magic||x.cycleId!=cycle||x.planId!=plan)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(x.accountLogin!=account||x.symbol!=symbol||x.magic!=magic||x.cycleId!=cycle||x.planId!=plan)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_IDENTITY_MISMATCH,\"HSBI-2D-ID\");"}
153 ADD {"id":"M153","name":"NO_OP_OWNERSHIP","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S027"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(!x.positionActuallyRead||!x.ownershipConfirmed)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_POSITION_NOT_CONFIRMED,\"HSBI-2D-POS\");","new":"if(!x.positionActuallyRead||!x.ownershipConfirmed)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(!x.positionActuallyRead||!x.ownershipConfirmed)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_POSITION_NOT_CONFIRMED,\"HSBI-2D-POS\");"}
154 ADD {"id":"M154","name":"NO_OP_PERSISTENCE","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S038"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(!x.persistencePrepared)return HSBI_RuntimeReject(x,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_RD_PERSISTENCE_REQUIRED,\"HSBI-2D-PERSIST\");","new":"if(!x.persistencePrepared)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(!x.persistencePrepared)return HSBI_RuntimeReject(x,HSBI_DECISION_PERSISTENCE_REQUIRED,HSBI_RD_PERSISTENCE_REQUIRED,\"HSBI-2D-PERSIST\");"}
155 ADD {"id":"M155","name":"NO_OP_DIGEST","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S039D"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.inputDigest==\"\"||x.inputDigest!=HSBI_RuntimeDecisionContextDigest(x))return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_DIGEST_MISMATCH,\"HSBI-2D-DIGEST\");","new":"if(x.inputDigest==\"\"||x.inputDigest!=HSBI_RuntimeDecisionContextDigest(x))return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(x.inputDigest==\"\"||x.inputDigest!=HSBI_RuntimeDecisionContextDigest(x))return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_DIGEST_MISMATCH,\"HSBI-2D-DIGEST\");"}
156 ADD {"id":"M156","name":"NO_OP_EVENT_ACTION","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S029"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.eventId==0||x.actionId==0)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,x.eventId==0?HSBI_RD_EVENT_NOT_FRESH:HSBI_RD_ACTION_ID_MISMATCH,\"HSBI-2D-EVENT\");","new":"if(x.eventId==0||x.actionId==0)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(x.eventId==0||x.actionId==0)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,x.eventId==0?HSBI_RD_EVENT_NOT_FRESH:HSBI_RD_ACTION_ID_MISMATCH,\"HSBI-2D-EVENT\");"}
157 ADD {"id":"M157","name":"NO_OP_SCHEMA","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S031"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.schemaVersion!=HSBI_SCHEMA_VERSION)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_SCHEMA_VERSION_MISMATCH,\"HSBI-2D-SCHEMA\");","new":"if(x.schemaVersion!=HSBI_SCHEMA_VERSION)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(x.schemaVersion!=HSBI_SCHEMA_VERSION)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_SCHEMA_VERSION_MISMATCH,\"HSBI-2D-SCHEMA\");"}
158 ADD {"id":"M158","name":"NO_OP_RECONCILIATION","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S034"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.reconciliationConflict)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_RECONCILIATION_CONFLICT,\"HSBI-2D-RECON\");","new":"if(x.reconciliationConflict)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(x.reconciliationConflict)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_RECONCILIATION_CONFLICT,\"HSBI-2D-RECON\");"}
159 ADD {"id":"M159","name":"NO_OP_TRANSACTION_BARRIER","target":"Include/Runtime/HSBI_RuntimeTransactionBarrier.mqh","mutation_type":"semantic","expected_check_ids":["S025"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(b.context.eventId<=b.expectedEventId)return HSBI_RuntimeReject(b.context,HSBI_DECISION_REJECTED,HSBI_RD_EVENT_NOT_FRESH,\"HSBI-2D-BARRIER-EVENT\");","new":"if(b.context.eventId<=b.expectedEventId)return HSBI_RuntimeReject(b.context,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(b.context.eventId<=b.expectedEventId)return HSBI_RuntimeReject(b.context,HSBI_DECISION_REJECTED,HSBI_RD_EVENT_NOT_FRESH,\"HSBI-2D-BARRIER-EVENT\");"}
160 ADD {"id":"M160","name":"S037_CONFLICT_STATUS","target":"Include/Runtime/HSBI_RuntimeRestartValidator.mqh","mutation_type":"semantic","expected_check_ids":["S037"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(s.duplicateConsumption)return HSBI_RuntimeReject(s.current,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"HSBI-2D-RESTART-NOOP\");","new":"if(s.duplicateConsumption)return HSBI_RuntimeReject(s.current,HSBI_DECISION_CONFLICT,HSBI_RD_OK,\"HSBI-2D-RESTART-NOOP\");"}
161 ADD {"id":"M161","name":"S037_WRONG_REASON","target":"Include/Runtime/HSBI_RuntimeRestartValidator.mqh","mutation_type":"semantic","expected_check_ids":["S037"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(s.duplicateConsumption)return HSBI_RuntimeReject(s.current,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"HSBI-2D-RESTART-NOOP\");","new":"if(s.duplicateConsumption)return HSBI_RuntimeReject(s.current,HSBI_DECISION_NO_OP,HSBI_RD_DOUBLE_COUNT_BLOCKED,\"HSBI-2D-RESTART-NOOP\");"}
162 ADD {"id":"M162","name":"NO_OP_WRONG_FUNCTION","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
163 ADD {"id":"M163","name":"DOUBLE_NEGATION_NO_OP","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(!!(revision!=x.stateRevision))return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
164 ADD {"id":"M164","name":"BOOLEAN_COMPARISON_NO_OP","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if((revision==x.stateRevision)==false)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
165 ADD {"id":"M165","name":"UNKNOWN_CONDITION_NO_OP","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":"if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":"if(HSBI_UnknownPredicate(x,revision))return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS\");if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
Removed trailing baseline records []
````

### Mutation catalog R7

````text
FILE Tests/Static/hsb_2d_v1_r7_mutations.json SHA256 41a06bd630105b4c92a1aee2a7f3dfc31c09c295e446400c4f7a7e2b00ab875b
BASE Tests/Static/hsb_2d_v1_r6_mutations.json SHA256 370ccb3e02bcbbdabc88b4bfa2a43aa59fd997a88d5e5bfc047b3994500b2051
Exact unchanged record ordinals [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 45, 46, 47, 48, 49, 50, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 67, 72, 77, 82, 87, 92, 97, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165]
39 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->"}
41 PATCH remove=[] set={"old":"METAEDITOR_MAIN_COMPILE=NOT_RUN"}
42 PATCH remove=[] set={"old":"MQL5_TESTS_T01_T464=NOT_RUN"}
43 PATCH remove=[] set={"old":"BROKER_MONEY_RUNTIME_PROOF=NOT_RUN"}
44 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R7_CANONICAL_STATUS_BEGIN"}
51 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R7_FILE_MANIFEST_SHA256.txt"}
52 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R7_FILE_MANIFEST_SHA256.txt"}
53 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R7_FILE_MANIFEST_SHA256.txt"}
54 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R7_FILE_MANIFEST_SHA256.txt"}
55 PATCH remove=[] set={"target":"Reports/HSB_2D_V1_R7_FILE_MANIFEST_SHA256.txt"}
66 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->"}
68 PATCH remove=[] set={"old":"METAEDITOR_MAIN_COMPILE=NOT_RUN"}
69 PATCH remove=[] set={"old":"MQL5_TESTS_T01_T464=NOT_RUN"}
70 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R7_CANONICAL_STATUS_BEGIN"}
71 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->"}
73 PATCH remove=[] set={"old":"METAEDITOR_MAIN_COMPILE=NOT_RUN"}
74 PATCH remove=[] set={"old":"MQL5_TESTS_T01_T464=NOT_RUN"}
75 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R7_CANONICAL_STATUS_BEGIN"}
76 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->"}
78 PATCH remove=[] set={"old":"METAEDITOR_MAIN_COMPILE=NOT_RUN"}
79 PATCH remove=[] set={"old":"MQL5_TESTS_T01_T464=NOT_RUN"}
80 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R7_CANONICAL_STATUS_BEGIN"}
81 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->"}
83 PATCH remove=[] set={"old":"METAEDITOR_MAIN_COMPILE=NOT_RUN"}
84 PATCH remove=[] set={"old":"MQL5_TESTS_T01_T464=NOT_RUN"}
85 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R7_CANONICAL_STATUS_BEGIN"}
86 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->"}
88 PATCH remove=[] set={"old":"METAEDITOR_MAIN_COMPILE=NOT_RUN"}
89 PATCH remove=[] set={"old":"MQL5_TESTS_T01_T464=NOT_RUN"}
90 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R7_CANONICAL_STATUS_BEGIN"}
91 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->"}
93 PATCH remove=[] set={"old":"METAEDITOR_MAIN_COMPILE=NOT_RUN"}
94 PATCH remove=[] set={"old":"MQL5_TESTS_T01_T464=NOT_RUN"}
95 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R7_CANONICAL_STATUS_BEGIN"}
96 PATCH remove=[] set={"old":"REAL_TRADING_ALLOWED=NO\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->","new":"REAL_TRADING_ALLOWED=YES\nHSB_2D_V1_R7_CANONICAL_STATUS_END -->"}
98 PATCH remove=[] set={"old":"METAEDITOR_MAIN_COMPILE=NOT_RUN"}
99 PATCH remove=[] set={"old":"MQL5_TESTS_T01_T464=NOT_RUN"}
100 PATCH remove=[] set={"old":"<!-- HSB_2D_V1_R7_CANONICAL_STATUS_BEGIN"}
101 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R7_CLEAN_RESULT.txt"}
102 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R7_MUTATION_RESULTS.json"}
103 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R7_EVIDENCE_SEAL_SHA256.txt"}
116 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R7_CLEAN_RESULT.txt"}
117 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R7_MUTATION_RESULTS.json","old":"\"schema\": \"HSB.2D-V1-R7/mutations/1\""}
118 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R7_MUTATION_RESULTS.txt"}
119 PATCH remove=[] set={"target":"Tests/Static/hsb_2d_v1_r7_mutations.json"}
120 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R7_EVIDENCE_SEAL_SHA256.txt"}
121 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R7_EVIDENCE_SEAL_SHA256.txt"}
122 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R7_EVIDENCE_SEAL_SHA256.txt"}
123 PATCH remove=[] set={"target":"Tests/Evidence/HSB_2D_V1_R7_EVIDENCE_SEAL_SHA256.txt"}
166 ADD {"id":"M166","name":"r7_terminal_bypass_166","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if(revision<x.stateRevision||revision>x.stateRevision)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS166\"); if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
167 ADD {"id":"M167","name":"r7_terminal_bypass_167","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if(revision>x.stateRevision||revision<x.stateRevision)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS167\"); if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
168 ADD {"id":"M168","name":"r7_terminal_bypass_168","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if(x.stateRevision<revision||x.stateRevision>revision)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS168\"); if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
169 ADD {"id":"M169","name":"r7_terminal_bypass_169","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if(!(revision==x.stateRevision))return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS169\"); if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
170 ADD {"id":"M170","name":"r7_terminal_bypass_170","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if((revision-x.stateRevision)!=0)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS170\"); if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
171 ADD {"id":"M171","name":"r7_terminal_bypass_171","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if(HSBI_UnknownPredicate(revision,x.stateRevision))return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS171\"); if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
172 ADD {"id":"M172","name":"r7_terminal_bypass_172","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if(revision==x.stateRevision){}else{return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS172\");} if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
173 ADD {"id":"M173","name":"r7_terminal_bypass_173","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" HSBI_RuntimeDecisionResult r=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,HSBI_RD_OK,\"HSBI-2D-VALID\");","new":" if(x.immutable)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS173\"); HSBI_RuntimeDecisionResult r=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,HSBI_RD_OK,\"HSBI-2D-VALID\");"}
174 ADD {"id":"M174","name":"r7_terminal_bypass_174","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if(revision<x.stateRevision||revision>x.stateRevision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_OK,\"BYPASS174\"); if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
175 ADD {"id":"M175","name":"r7_terminal_bypass_175","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if(revision<x.stateRevision||revision>x.stateRevision)return HSBI_RuntimeReject(x,HSBI_DECISION_REJECTED,HSBI_RD_STATE_REVISION_MISMATCH,\"BYPASS175\"); if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
176 ADD {"id":"M176","name":"r7_terminal_bypass_176","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if(s.duplicateConsumption)return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS176\"); if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
177 ADD {"id":"M177","name":"r7_s037_wrong_reason","target":"Include/Runtime/HSBI_RuntimeRestartValidator.mqh","mutation_type":"semantic","expected_check_ids":["S037"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(s.duplicateConsumption)return HSBI_RuntimeReject(s.current,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"HSBI-2D-RESTART-NOOP\");","new":" if(s.duplicateConsumption)return HSBI_RuntimeReject(s.current,HSBI_DECISION_NO_OP,HSBI_RD_CONTEXT_INVALID,\"HSBI-2D-RESTART-NOOP\");"}
178 ADD {"id":"M178","name":"r7_terminal_bypass_178","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\"); if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
179 ADD {"id":"M179","name":"r7_terminal_bypass_179","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if(revision<x.stateRevision||revision>x.stateRevision)return HSBI_UnknownDecisionHelper(x); if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
180 ADD {"id":"M180","name":"r7_terminal_bypass_180","target":"Include/Runtime/HSBI_RuntimeDecisionValidator.mqh","mutation_type":"semantic","expected_check_ids":["S028"],"expected_exit":"nonzero","manifest_strategy":"rehash_mutated_file","required":true,"old":" if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");","new":" if(revision<x.stateRevision||revision>x.stateRevision)return x.immutable?HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,\"BYPASS180\"):HSBI_UnknownDecisionHelper(x); if(x.stateRevision!=revision)return HSBI_RuntimeReject(x,HSBI_DECISION_CONFLICT,HSBI_RD_STATE_REVISION_MISMATCH,\"HSBI-2D-REV\");"}
181 ADD {"id":"M181","name":"r7_evidence_181","target":"Tests/Evidence/HSB_2D_V1_R7_ADVERSARIAL_RESULTS.json","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"\"schema\": \"HSB.2D-V1-R7/adversarial/1\"","new":"\"schema\": \"TAMPERED\""}
182 ADD {"id":"M182","name":"r7_evidence_182","target":"Tests/Evidence/HSB_2D_V1_R7_TERMINAL_PATH_PROOFS.json","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"\"schema\": \"HSB.2D-V1-R7/terminal-paths/1\"","new":"\"schema\": \"REMOVED\""}
183 ADD {"id":"M183","name":"r7_evidence_183","target":"Tests/Evidence/HSB_2D_V1_R7_TERMINAL_PATH_PROOFS.json","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"\"evidence_hash\": \"VALID\"","new":"\"evidence_hash\": \"TAMPERED\""}
184 ADD {"id":"M184","name":"r7_evidence_184","target":"Tests/Evidence/HSB_2D_V1_R7_EVIDENCE_SEAL_SHA256.txt","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"__ADD_EXTRA__","new":"__ADD_EXTRA__"}
185 ADD {"id":"M185","name":"r7_evidence_185","target":"Tests/Evidence/HSB_2D_V1_R7_EVIDENCE_SEAL_SHA256.txt","mutation_type":"evidence","expected_check_ids":["S046E"],"expected_exit":"nonzero","manifest_strategy":"none","required":true,"old":"__REMOVE_FIRST__","new":"__REMOVE_FIRST__"}
Removed trailing baseline records []
````

## R3 — полные line-reference представления исторических manifests

Каждая ссылка @BASE_LINE означает побуквенно совпавшую ранее прочитанную строку предыдущего manifest; все остальные строки приведены полностью. Порядок текущих строк сохранён; это не whole-file duplicate и не семантическая проверка перечисленных файлов.

### Manifest R1

````text
FILE Reports/HSB_2D_V1_R1_FILE_MANIFEST_SHA256.txt SHA256 f7b57d3c1a33dc2ac1fcc7b6565c430f23e2a969a64143c3f7179ea75ea6ae4f
BASE Reports/HSB_2D_V1_FILE_MANIFEST_SHA256.txt
1: e5f2614cc3758d95b1e2445f85609f0971e1fab2ee5dcbb1caf6ee277edb4c2c  BUILD_INFO.md
2: 90d78209a83317f7a901e73b19abc942113ded721b96d9f25e657f272cb56e24  CHANGELOG_RU.md
3: 101c5b6f1c1de0a8dcbcf03149f191ab7bd777c316f284362c6939e011d7c1b2  Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md
4: ff7dd2da6080129e830ad8627a01a0354a31386854faa2b942764e38ae7924fb  Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md
5: 46e744a88d2e74c3aac2292b789f217eef4e3ef475dae13e80e4d537d9416813  Docs/22_OPEN_DECISIONS_REGISTER_RU.md
6: @BASE_LINE(6)
7: @BASE_LINE(7)
8: @BASE_LINE(8)
9: @BASE_LINE(9)
10: @BASE_LINE(10)
11: @BASE_LINE(11)
12: @BASE_LINE(12)
13: @BASE_LINE(13)
14: @BASE_LINE(14)
15: @BASE_LINE(15)
16: @BASE_LINE(16)
17: @BASE_LINE(17)
18: @BASE_LINE(18)
19: @BASE_LINE(19)
20: @BASE_LINE(20)
21: @BASE_LINE(21)
22: @BASE_LINE(22)
23: @BASE_LINE(23)
24: @BASE_LINE(24)
25: @BASE_LINE(25)
26: @BASE_LINE(26)
27: @BASE_LINE(27)
28: @BASE_LINE(28)
29: @BASE_LINE(29)
30: @BASE_LINE(30)
31: @BASE_LINE(31)
32: @BASE_LINE(32)
33: @BASE_LINE(33)
34: @BASE_LINE(34)
35: @BASE_LINE(35)
36: @BASE_LINE(36)
37: @BASE_LINE(37)
38: @BASE_LINE(38)
39: @BASE_LINE(39)
40: @BASE_LINE(40)
41: @BASE_LINE(41)
42: @BASE_LINE(42)
43: @BASE_LINE(43)
44: @BASE_LINE(44)
45: @BASE_LINE(45)
46: @BASE_LINE(46)
47: @BASE_LINE(47)
48: @BASE_LINE(48)
49: @BASE_LINE(49)
50: @BASE_LINE(50)
51: @BASE_LINE(51)
52: @BASE_LINE(52)
53: @BASE_LINE(53)
54: @BASE_LINE(54)
55: @BASE_LINE(55)
56: @BASE_LINE(56)
57: @BASE_LINE(57)
58: @BASE_LINE(58)
59: @BASE_LINE(59)
60: @BASE_LINE(60)
61: @BASE_LINE(61)
62: @BASE_LINE(62)
63: @BASE_LINE(63)
64: @BASE_LINE(64)
65: @BASE_LINE(65)
66: @BASE_LINE(66)
67: @BASE_LINE(67)
68: @BASE_LINE(68)
69: @BASE_LINE(69)
70: @BASE_LINE(70)
71: @BASE_LINE(71)
72: @BASE_LINE(72)
73: @BASE_LINE(73)
74: @BASE_LINE(74)
75: @BASE_LINE(75)
76: @BASE_LINE(76)
77: @BASE_LINE(77)
78: @BASE_LINE(78)
79: @BASE_LINE(79)
80: @BASE_LINE(80)
81: 35a219c8c7a652c28fe6f2385c2eb5c4b9c43954ab600fa77ac78450a04a241f  PROJECT_MAP_RU.md
82: 85832205a003a8f50528810e27d84c405d649e351257ee2c8fb5113f46b6ed0a  README_RU.md
83: a293ec51de6ffecfd9f0e7780e2ac8d27d4c2fa9001175ee233a509197d98da7  Reports/HSB_2D_V1_R1_FINAL_OFFLINE_ACCEPTANCE_RU.md
84: 7b91f0a89ef549a5497f872cb0cc6aee9e630fa3d247e460dc4259f5ccbb6e17  Reports/HSB_2D_V1_R1_FRESH_CLONE_BASELINE_RU.md
85: 43ed22d44d4723eeb3beb1cee2b897bd6cf68a7f2b5597ee96fdb4d136b3a852  Reports/HSB_2D_V1_R1_MANIFEST_AUDIT_RU.md
86: a1a478ff3695d195d94a90b2c12048953a5e0781c1c8b11754e33376268a1ba6  Reports/HSB_2D_V1_R1_MUTATION_AUDIT_RU.md
87: b4379c97a13163c1bc2da9ff3eb4983369ecafda9c4266aaff5454344f23e49a  Reports/HSB_2D_V1_R1_REOPENING_RU.md
88: 6f8b670f2278b72df4ca9cac414cd2936616e905054066b71d618a02a7802bae  Reports/HSB_2D_V1_R1_RUNTIME_CONTRACT_AUDIT_RU.md
89: 17bf37c288272f30d64dd3143157032b4df9997eeefa213b68ff173bf1cf02ad  Reports/HSB_2D_V1_R1_TRACEABILITY_MATRIX_RU.md
90: ea7311de9b892ee62efa93e1aa772c49593b626d858697c1fdc2122b5c8d1a0e  Reports/HSB_2D_V1_R1_VERIFIER_ARCHITECTURE_RU.md
91: @BASE_LINE(84)
92: 040628d4dd0d4d6d9476d9b6639f8e2c9a0d5d1a5d126e2fb029a2cc7890f439  Tests/Static/hsb_2d_v1_include_graph.json
93: 7dca6cadc5cb10bde4172def761d309a9b9ce491d335c6d5e415f4f1452a231d  Tests/Static/hsb_2d_v1_r1_mutations.json
94: 295ce2a8616a7f5d07a286e7f2d671828d28c369eeb534881d83898d379b50d1  Tests/Static/run_hsb_2d_v1_r1_mutations.py
95: bf73945f3d314708a4801ab41cab4d548258019139bd2f0e398f03e48d082ff9  Tests/Static/verify_hsb_2d_v1.py
96: 1779d3c790a955b9ff8be3c24241b2d991687c6e8a9bab8859d70fa4b1a61473  Tests/Static/verify_hsb_2d_v1_r1.py
97: # SELF_REFERENCE_EXCLUDED=Reports/HSB_2D_V1_R1_FILE_MANIFEST_SHA256.txt
98: # GENERATED_EVIDENCE_EXCLUDED=Tests/Evidence/HSB_2D_V1_R1_CLEAN_RESULT.txt,Tests/Evidence/HSB_2D_V1_R1_MUTATION_RESULTS.json,Tests/Evidence/HSB_2D_V1_R1_MUTATION_RESULTS.txt
99: # PUBLICATION_SELF_REFERENCE_EXCLUDED=Reports/HSB_2D_V1_R1_FINAL_PUBLICATION_RECORD_RU.md

````

### Manifest R2

````text
FILE Reports/HSB_2D_V1_R2_FILE_MANIFEST_SHA256.txt SHA256 a03a5f8fa83b08cea9b11c2e1f4eb28ea1f84e534908732b12b46fdb96950c45
BASE Reports/HSB_2D_V1_R1_FILE_MANIFEST_SHA256.txt
1: ab965c3b4fefa867105f773b94cc351ef5af44673f60eb8fdfbf47fb4b7e629e  BUILD_INFO.md
2: 96c6072b6ab8df2057a0a11466ee7bdbab30c552ac9eb670f0e865f1a039cd2a  CHANGELOG_RU.md
3: 1ac6feffaed5ff4843bbc9c5d4a8837b7f392c0c10e2e69274eed2f094004453  Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md
4: 9f3c3bfb51e1acd8560e03fe93a0a4ce729c9bcf799d0cd2bca623a5cdd41d00  Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md
5: 9e85f438e1e3b7a0afc18f0c807100ad6dddca0475eeaa998e01da9aa92c947a  Docs/22_OPEN_DECISIONS_REGISTER_RU.md
6: @BASE_LINE(6)
7: @BASE_LINE(7)
8: @BASE_LINE(8)
9: @BASE_LINE(9)
10: @BASE_LINE(10)
11: @BASE_LINE(11)
12: @BASE_LINE(12)
13: @BASE_LINE(13)
14: @BASE_LINE(14)
15: @BASE_LINE(15)
16: @BASE_LINE(16)
17: @BASE_LINE(17)
18: @BASE_LINE(18)
19: @BASE_LINE(19)
20: @BASE_LINE(20)
21: @BASE_LINE(21)
22: @BASE_LINE(22)
23: @BASE_LINE(23)
24: @BASE_LINE(24)
25: @BASE_LINE(25)
26: @BASE_LINE(26)
27: @BASE_LINE(27)
28: @BASE_LINE(28)
29: @BASE_LINE(29)
30: @BASE_LINE(30)
31: @BASE_LINE(31)
32: @BASE_LINE(32)
33: @BASE_LINE(33)
34: @BASE_LINE(34)
35: @BASE_LINE(35)
36: @BASE_LINE(36)
37: @BASE_LINE(37)
38: @BASE_LINE(38)
39: @BASE_LINE(39)
40: @BASE_LINE(40)
41: @BASE_LINE(41)
42: @BASE_LINE(42)
43: @BASE_LINE(43)
44: @BASE_LINE(44)
45: @BASE_LINE(45)
46: @BASE_LINE(46)
47: @BASE_LINE(47)
48: @BASE_LINE(48)
49: @BASE_LINE(49)
50: @BASE_LINE(50)
51: @BASE_LINE(51)
52: @BASE_LINE(52)
53: @BASE_LINE(53)
54: @BASE_LINE(54)
55: @BASE_LINE(55)
56: @BASE_LINE(56)
57: @BASE_LINE(57)
58: @BASE_LINE(58)
59: @BASE_LINE(59)
60: @BASE_LINE(60)
61: @BASE_LINE(61)
62: @BASE_LINE(62)
63: @BASE_LINE(63)
64: @BASE_LINE(64)
65: @BASE_LINE(65)
66: @BASE_LINE(66)
67: @BASE_LINE(67)
68: @BASE_LINE(68)
69: @BASE_LINE(69)
70: @BASE_LINE(70)
71: @BASE_LINE(71)
72: @BASE_LINE(72)
73: @BASE_LINE(73)
74: @BASE_LINE(74)
75: @BASE_LINE(75)
76: @BASE_LINE(76)
77: @BASE_LINE(77)
78: @BASE_LINE(78)
79: @BASE_LINE(79)
80: @BASE_LINE(80)
81: 388f26ee057e7863ed2892d234686fca6aa8e3fb11a760d15a91cf4ba759bf59  PROJECT_MAP_RU.md
82: 4d546f9780aa788e12902783dea3c049b126a1dd91ac97a28a910f5da7154527  README_RU.md
83: 5ff00e93a9edb3511fa01edc8a410db7660c7170df91b3252656a0310348876e  Reports/HSB_2D_V1_R2_COMMENT_AWARE_AUDIT_RU.md
84: 3f3e265bd7e3dd889b7ca4dee31b85572ab1d24505baffae52e8be29b2f99f0f  Reports/HSB_2D_V1_R2_EVIDENCE_INTEGRITY_RU.md
85: f32a345e42fb99bc2c8471a5c2daa5c5780e540bfea9b39735ae7af54bd9138e  Reports/HSB_2D_V1_R2_FINAL_OFFLINE_ACCEPTANCE_RU.md
86: 2a1fbc09ebc78ae2e080e0f1b5efe795a3269969aa25e176143d2fa9b4b286a1  Reports/HSB_2D_V1_R2_LEXER_ARCHITECTURE_RU.md
87: 170f0e0adeeb49945c11ba529780f2aaf02b42b61587c206c2e92558bd548015  Reports/HSB_2D_V1_R2_MUTATION_AUDIT_RU.md
88: 8cd7b2cc3cb25904aff4dda70b7d24730a2e92b0b1835ef6357d52b2a46ad621  Reports/HSB_2D_V1_R2_REOPENING_RU.md
89: 207c72ad064e5b68541aed53aa1853afd35f007a268d80a39812df6407cdee75  Reports/HSB_2D_V1_R2_STATUS_DOCUMENT_AUDIT_RU.md
90: 776626610ab32e22fa4bfc5150ec78d656a4670470edf7c5bb0452a9e1e229f0  Reports/HSB_2D_V1_R2_TRACEABILITY_MATRIX_RU.md
91: @BASE_LINE(91)
92: @BASE_LINE(92)
93: @BASE_LINE(93)
94: b12d49d18bf4f69ebd811cf4ba96836cfc33ca73ce7ab2ca74c63dd67fa01c0b  Tests/Static/hsb_2d_v1_r2_mutations.json
95: e3753dac6808d75bac5d1ab2080570f07b07b6477ecf33e1c8d82154dbc92225  Tests/Static/hsb_mql5_lexer.py
96: @BASE_LINE(94)
97: ebc3a557da14d29475e359abad31b1e822676efd33bbe06917a475e28422bc79  Tests/Static/run_hsb_2d_v1_r2_mutations.py
98: @BASE_LINE(95)
99: @BASE_LINE(96)
100: 3bea4de358c50219203142328fa178b4e341cda5aa4ea8e870e9fb4bb25ab739  Tests/Static/verify_hsb_2d_v1_r2.py
101: # SELF_REFERENCE_EXCLUDED=Reports/HSB_2D_V1_R2_FILE_MANIFEST_SHA256.txt
102: # SEALED_EVIDENCE_EXCLUDED_FROM_MANIFEST=Tests/Evidence/HSB_2D_V1_R2_EVIDENCE_SEAL_SHA256.txt

````

### Manifest R3

````text
FILE Reports/HSB_2D_V1_R3_FILE_MANIFEST_SHA256.txt SHA256 bbaa212d09e13b7a121c21e8b01aac7b478f77e0436998629e5df978470a349c
BASE Reports/HSB_2D_V1_R2_FILE_MANIFEST_SHA256.txt
1: 31125ef18dc0aeacd3b5d57786e59ed9c93b744621113c88202dc98f2fb67eee  BUILD_INFO.md
2: ee3d7edb856682451fc5355618d3a887d3ff85e053d3fad66c3f5ae7754a1b08  CHANGELOG_RU.md
3: 00e63c67919d79acb380b5ec5cee026c0c80a4e1828448e450589f7f14c73f70  Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md
4: 365d90fb865c6e715657ed571ea439a38f44e424971985db5a8f88ddacc8713b  Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md
5: a83b1a881755ea6e968f01410c81eb933944c3618a2475f92efe03053048d4c7  Docs/22_OPEN_DECISIONS_REGISTER_RU.md
6: @BASE_LINE(7)
7: @BASE_LINE(8)
8: @BASE_LINE(9)
9: @BASE_LINE(10)
10: @BASE_LINE(11)
11: @BASE_LINE(12)
12: @BASE_LINE(13)
13: @BASE_LINE(14)
14: @BASE_LINE(15)
15: @BASE_LINE(16)
16: @BASE_LINE(17)
17: @BASE_LINE(18)
18: @BASE_LINE(19)
19: @BASE_LINE(20)
20: @BASE_LINE(21)
21: @BASE_LINE(22)
22: @BASE_LINE(23)
23: @BASE_LINE(24)
24: @BASE_LINE(25)
25: @BASE_LINE(26)
26: @BASE_LINE(27)
27: @BASE_LINE(28)
28: @BASE_LINE(29)
29: @BASE_LINE(30)
30: @BASE_LINE(31)
31: @BASE_LINE(32)
32: @BASE_LINE(33)
33: @BASE_LINE(34)
34: @BASE_LINE(35)
35: @BASE_LINE(36)
36: @BASE_LINE(37)
37: @BASE_LINE(38)
38: @BASE_LINE(39)
39: @BASE_LINE(40)
40: @BASE_LINE(41)
41: @BASE_LINE(42)
42: @BASE_LINE(43)
43: @BASE_LINE(44)
44: @BASE_LINE(45)
45: @BASE_LINE(46)
46: @BASE_LINE(47)
47: @BASE_LINE(48)
48: @BASE_LINE(49)
49: @BASE_LINE(50)
50: @BASE_LINE(51)
51: @BASE_LINE(52)
52: @BASE_LINE(53)
53: @BASE_LINE(54)
54: @BASE_LINE(55)
55: @BASE_LINE(56)
56: @BASE_LINE(57)
57: @BASE_LINE(58)
58: @BASE_LINE(59)
59: @BASE_LINE(60)
60: @BASE_LINE(61)
61: @BASE_LINE(62)
62: @BASE_LINE(63)
63: @BASE_LINE(64)
64: @BASE_LINE(65)
65: @BASE_LINE(66)
66: @BASE_LINE(67)
67: @BASE_LINE(68)
68: @BASE_LINE(69)
69: @BASE_LINE(70)
70: @BASE_LINE(71)
71: @BASE_LINE(72)
72: @BASE_LINE(73)
73: @BASE_LINE(74)
74: @BASE_LINE(75)
75: @BASE_LINE(76)
76: @BASE_LINE(77)
77: @BASE_LINE(78)
78: @BASE_LINE(79)
79: @BASE_LINE(80)
80: 74fcba3d30dcbae8dbedef51c50eddcf94f992455ca3eb301f6e5b3f0add27fa  PROJECT_MAP_RU.md
81: 64fae1d13cd99857b2d279a57cb334de9a7a7b2383140999795edf4b9e9d8ef0  README_RU.md
82: ca0e42764215c00f07d155b4c7277138e908289f1424ede771603afd0a6c234a  Reports/HSB_2D_V1_R3_FALSE_PASS_ANALYSIS_RU.md
83: ea310d8770064407fdd63d09f6ff3426cf75d7814658f5aa58636cf8b25f3bd8  Reports/HSB_2D_V1_R3_FINAL_VERDICT_RU.md
84: 5006a309a7ff3406c20e8658e904ed4bbc8e79f448af3ffa2aa4c295a316c8fe  Reports/HSB_2D_V1_R3_REACHABILITY_ARCHITECTURE_RU.md
85: 669a46f99b1e97bd02c8f0633c374d6fbe1f95295e174ad6da8600899d517b51  Reports/HSB_2D_V1_R3_REOPENING_RU.md
86: @BASE_LINE(91)
87: 01aa8826cd2791d00bce13fa6b69392e5dc6560500443e83a7b9d61a5c2bbaac  Tests/Static/hsb_mql5_lexer.py
88: 0047be86df5a64fdd2d7ce25cc12ddc719788b7e5d1c0828c2c3890bbc06da6a  Tests/Static/run_hsb_2d_v1_r3_mutations.py
89: 997074ab43be224af688aa59d2afbc8fe54fd392d5781353bf98a7bdf3c9e9cd  Tests/Static/verify_hsb_2d_v1_r3.py

````

### Manifest R4

````text
FILE Reports/HSB_2D_V1_R4_FILE_MANIFEST_SHA256.txt SHA256 3890495b700284b3e7973a068fa45d1322253a8f85249b62a554a163e9e4376a
BASE Reports/HSB_2D_V1_R3_FILE_MANIFEST_SHA256.txt
1: eab1ea27618748e6238ec18cc1fa520a6726c645d14434a2a80741dd47148c70  BUILD_INFO.md
2: aa2808d23439e5971462c68a7d4f98c99400953b7779448216ca60d50cfd276b  CHANGELOG_RU.md
3: 9132a746062629a23af1940f9026d856e36b5bdae1372177b083b7670d869a9e  Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md
4: 98562cd84944765e4e1fdf9accedc51b2c9e3b32629bda940c9eaa4804c8de0c  Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md
5: 218e4d0c262bad9ea845b6cfa1c97d81e438d6442b13c88d72c0f9486e7379cb  Docs/22_OPEN_DECISIONS_REGISTER_RU.md
6: @BASE_LINE(6)
7: @BASE_LINE(7)
8: @BASE_LINE(8)
9: @BASE_LINE(9)
10: @BASE_LINE(10)
11: @BASE_LINE(11)
12: @BASE_LINE(12)
13: @BASE_LINE(13)
14: @BASE_LINE(14)
15: @BASE_LINE(15)
16: @BASE_LINE(16)
17: @BASE_LINE(17)
18: @BASE_LINE(18)
19: @BASE_LINE(19)
20: @BASE_LINE(20)
21: @BASE_LINE(21)
22: @BASE_LINE(22)
23: @BASE_LINE(23)
24: @BASE_LINE(24)
25: @BASE_LINE(25)
26: @BASE_LINE(26)
27: @BASE_LINE(27)
28: @BASE_LINE(28)
29: @BASE_LINE(29)
30: @BASE_LINE(30)
31: @BASE_LINE(31)
32: @BASE_LINE(32)
33: @BASE_LINE(33)
34: @BASE_LINE(34)
35: @BASE_LINE(35)
36: @BASE_LINE(36)
37: @BASE_LINE(37)
38: @BASE_LINE(38)
39: @BASE_LINE(39)
40: @BASE_LINE(40)
41: @BASE_LINE(41)
42: @BASE_LINE(42)
43: @BASE_LINE(43)
44: @BASE_LINE(44)
45: @BASE_LINE(45)
46: @BASE_LINE(46)
47: @BASE_LINE(47)
48: @BASE_LINE(48)
49: @BASE_LINE(49)
50: @BASE_LINE(50)
51: @BASE_LINE(51)
52: @BASE_LINE(52)
53: @BASE_LINE(53)
54: @BASE_LINE(54)
55: @BASE_LINE(55)
56: @BASE_LINE(56)
57: @BASE_LINE(57)
58: @BASE_LINE(58)
59: @BASE_LINE(59)
60: @BASE_LINE(60)
61: @BASE_LINE(61)
62: @BASE_LINE(62)
63: @BASE_LINE(63)
64: @BASE_LINE(64)
65: @BASE_LINE(65)
66: @BASE_LINE(66)
67: @BASE_LINE(67)
68: @BASE_LINE(68)
69: @BASE_LINE(69)
70: @BASE_LINE(70)
71: @BASE_LINE(71)
72: @BASE_LINE(72)
73: @BASE_LINE(73)
74: @BASE_LINE(74)
75: @BASE_LINE(75)
76: @BASE_LINE(76)
77: @BASE_LINE(77)
78: @BASE_LINE(78)
79: @BASE_LINE(79)
80: e0b3658030acb8c1b8ae1d0834e51911e409ce778d6fff5ff78f4ad7ba3f9006  PROJECT_MAP_RU.md
81: 1f4283e601ff8aea1d44f36ea8c43a001f91992f285f1b14a45e7d19a059c948  README_RU.md
82: e13c347e37c18bfbf38ab7775d8a8aeae5b6133e61af370dd97076c273decb2a  Reports/HSB_2D_V1_R4_CONDITIONAL_EARLY_SUCCESS_ANALYSIS_RU.md
83: b17f5e37a2793c2da636cc1b6dfaed24fa68b65244cbdbbeef10daa965f33d20  Reports/HSB_2D_V1_R4_CONTROL_FLOW_ARCHITECTURE_RU.md
84: 1b4c69fc0c3b1360fd3836f224a2c308ee554f2d902ee82183df57b62dc69cac  Reports/HSB_2D_V1_R4_FINAL_VERDICT_RU.md
85: 16d0f54caa632faece2654d8c7314081c58dd6ed2d34cc4ebea2a707f48d9f13  Reports/HSB_2D_V1_R4_MUTATION_AUDIT_RU.md
86: ee7b23e5ae8da382c05ff5f921391b5dd172790b738d3680c72f7ebfa5213a37  Reports/HSB_2D_V1_R4_REOPENING_RU.md
87: @BASE_LINE(86)
88: cb3f8fef65299cee89c51f73761262993f34bbb4fe194577ec9814ceef0c21b1  Tests/Static/hsb_2d_v1_r4_mutations.json
89: 651737eac65763cc79adbe575e806e36755d0297026cf727fe65fe2f53d2f76b  Tests/Static/hsb_mql5_lexer.py
90: 4ad3a0bc7df064964547c86f9942515ed90ac8aa1f170208a47df8ee88900c3d  Tests/Static/run_hsb_2d_v1_r4_mutations.py
91: 085aa7d1365ebd840360cb51985ebb5bb21a0b30dfe25befa388ad14192e49ca  Tests/Static/verify_hsb_2d_v1_r4.py

````

### Manifest R5

````text
FILE Reports/HSB_2D_V1_R5_FILE_MANIFEST_SHA256.txt SHA256 3125d2d3e919bf60f560e29b24960697e4fa21e3c04953430485ac2b67c5b416
BASE Reports/HSB_2D_V1_R4_FILE_MANIFEST_SHA256.txt
1: d242e76bc6a612848ae67ca36dd800fbd6b2269909e539ed1d13869033ea2da9  BUILD_INFO.md
2: bb638c64dbb2b7d816af5213c4a299a7848c46e2e87cf386afeb3bc9835efe18  CHANGELOG_RU.md
3: d644ad9e941a2ad17df61fa5fea8457e48ccfce119cc70f52674950f6643dd6d  Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md
4: 12bb5870ddb515794ed1cdd76783c6425913eebcd725529b0eff03ff5516bb03  Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md
5: 73606ba94d305df59c5e57186360df89a38b02ad947dfa4b8dbaa612852d4d49  Docs/22_OPEN_DECISIONS_REGISTER_RU.md
6: 60482eddee4020727145e895c1809747f266b3ddd09588456dbce6393855b45a  Docs/HSB_2D_ALLOCATION_CONSUMPTION_RUNTIME_RU.md
7: c9e91e57410a4cc6a0d32fa036707c638c6d98097be72a22a74b10c604424454  Docs/HSB_2D_PERSISTENCE_RESTART_CONTRACT_RU.md
8: 1a9c04d0f1675be361b479aa70aff0857a874eb4bfce23c7f42a7ea786f5d0ac  Docs/HSB_2D_RUNTIME_INTEGRATION_RU.md
9: d8ba4fc9fa1895485900fb71b290126a92c9bf3d211315f9b7c063d432fc54a4  Docs/HSB_2D_TRANSACTION_BARRIER_RU.md
10: 8098099aff8c950724b1996c21283904e7495ba91e4ad5ad9466d57130c87afb  Docs/HSB_2D_V2_EXACT_TEST_PROCEDURE_RU.md
11: 7752924012b3b38d74c276b70483b662b4d97994db42edcabd22c92b65ee6c05  Docs/HSB_2D_V2_METAEDITOR_USER_VERIFICATION_RU.md
12: eaf1e98ea2fcafb68af3e40d26e6a64e8a373510f66705ba3eb9f9e7190e2ecc  Docs/HSB_2D_V2_REQUIRED_EVIDENCE_CHECKLIST_RU.md
13: 36fefcc8dca62a459b994b7f3650047722c25cb561c7b6a3e919d838848a375a  Docs/HSB_2E_DEPENDENCY_GRAPH_RU.md
14: bcd9ac2ae9bbb36db93752e83599da42112518d470ee1683700b4e2318eee7aa  Docs/HSB_2E_FULL_TRADING_LOGIC_IMPLEMENTATION_PLAN_RU.md
15: 058414310cb1e06879b7f0733c445c13ffed69b82d649be8d4da059ad2bd4c5c  Docs/HSB_2E_PRODUCTION_FILE_MAP_RU.md
16: ed5bb5f13497102bfc069a4e24d1966d8a348ff6376515ea1b9bacd7a6f4ecf3  Docs/HSB_2E_SIMULATION_FIRST_ARCHITECTURE_RU.md
17: cf554f2c7f1c54eae2cfb96ede1751be796188e60f06f073865864fb07f07fe7  Docs/HSB_2E_TEST_MATRIX_RU.md
18: @BASE_LINE(6)
19: @BASE_LINE(7)
20: @BASE_LINE(8)
21: @BASE_LINE(9)
22: @BASE_LINE(10)
23: @BASE_LINE(11)
24: @BASE_LINE(12)
25: @BASE_LINE(13)
26: @BASE_LINE(14)
27: @BASE_LINE(15)
28: @BASE_LINE(16)
29: @BASE_LINE(17)
30: @BASE_LINE(18)
31: @BASE_LINE(19)
32: @BASE_LINE(20)
33: @BASE_LINE(21)
34: @BASE_LINE(22)
35: @BASE_LINE(23)
36: @BASE_LINE(24)
37: @BASE_LINE(25)
38: @BASE_LINE(26)
39: @BASE_LINE(27)
40: @BASE_LINE(28)
41: @BASE_LINE(29)
42: @BASE_LINE(30)
43: @BASE_LINE(31)
44: @BASE_LINE(32)
45: @BASE_LINE(33)
46: @BASE_LINE(34)
47: @BASE_LINE(35)
48: @BASE_LINE(36)
49: @BASE_LINE(37)
50: @BASE_LINE(38)
51: @BASE_LINE(39)
52: @BASE_LINE(40)
53: @BASE_LINE(41)
54: @BASE_LINE(42)
55: @BASE_LINE(43)
56: @BASE_LINE(44)
57: @BASE_LINE(45)
58: @BASE_LINE(46)
59: @BASE_LINE(47)
60: @BASE_LINE(48)
61: @BASE_LINE(49)
62: @BASE_LINE(50)
63: @BASE_LINE(51)
64: @BASE_LINE(52)
65: @BASE_LINE(53)
66: @BASE_LINE(54)
67: @BASE_LINE(55)
68: @BASE_LINE(56)
69: @BASE_LINE(57)
70: @BASE_LINE(58)
71: @BASE_LINE(59)
72: @BASE_LINE(60)
73: @BASE_LINE(61)
74: @BASE_LINE(62)
75: @BASE_LINE(63)
76: @BASE_LINE(64)
77: @BASE_LINE(65)
78: @BASE_LINE(66)
79: @BASE_LINE(67)
80: @BASE_LINE(68)
81: @BASE_LINE(69)
82: @BASE_LINE(70)
83: @BASE_LINE(71)
84: @BASE_LINE(72)
85: @BASE_LINE(73)
86: @BASE_LINE(74)
87: @BASE_LINE(75)
88: @BASE_LINE(76)
89: @BASE_LINE(77)
90: @BASE_LINE(78)
91: @BASE_LINE(79)
92: b41afedf3e7ab4f977aac38840459c18ee4f706b732f1dfa5392c1a34f993bb9  PROJECT_MAP_RU.md
93: 3dc14afd5358ea3ac217de53a5885622982fdb7aa4cb6582c4774909bf86e561  README_RU.md
94: cf846861e3305b3e731b71ab0a4c54076aa158b2666bc7c3e1122dda12782aa1  Reports/HSB_2D_V1_R5_FALSE_PASS_ANALYSIS_RU.md
95: a3934561eceadb3b8f694dbe8481b542144f8bea2c55f66ab11bcee45ca70971  Reports/HSB_2D_V1_R5_FINAL_VERDICT_RU.md
96: 0ff1a2c8ba366098de9f12967495e4215b5439f0026e7566e36903fcaa8e5f6c  Reports/HSB_2D_V1_R5_MUTATION_AUDIT_RU.md
97: 5d3b22acfb19d95fbd045d2de8b60755e1266ff318d50287717991c23ee46ca5  Reports/HSB_2D_V1_R5_REOPENING_RU.md
98: b35df2dcd4490a334e93ccc24a10945cf32c08872df2e6048fe786d4b10d3b50  Reports/HSB_2D_V2_USER_RESULT_TEMPLATE_RU.md
99: 1e47226c802ecf41fc42299c8779a47c3cea100fd20d04e2063e461c6f64e3f2  Reports/HSB_2E_PRE_IMPLEMENTATION_GAP_ANALYSIS_RU.md
100: @BASE_LINE(87)
101: 683d19672baa21b602a11b6a156adb813268e0a6a811cd32264f36d347e8a513  Tests/Static/hsb_2d_v1_r5_mutations.json
102: 7e9422cd8a0063c2da7c7905545bd57339718978dabf8818d9c204d5a600554b  Tests/Static/hsb_2e_expected_dependency_graph.json
103: e05fe9a881763fe881f0ca62831fd0709fb26838ee044b998d98543d4da6004e  Tests/Static/hsb_2e_test_plan.json
104: e9b8e0725de2ad86e749fc7e53a484320e64e5435b40c89185e0f9d1e1d06d60  Tests/Static/hsb_mql5_lexer.py
105: 4a38865b75acf7a8e2b21bb335dd7e8e40b7fde3a1772f1d67ffb0c29928f10b  Tests/Static/run_hsb_2d_v1_r5_mutations.py
106: 0bd490db4442d0bd3763ee34efa60a1fd588caf28385342351fa136bfd9c7f43  Tests/Static/verify_hsb_2d_v1_r5.py
107: 4e020ef2fe83bfe7b518d9a88619548881fb20b59ce5178e00393f393c8a66d2  Tests/Static/verify_hsb_2d_v2_user_evidence.py

````

### Manifest R6

````text
FILE Reports/HSB_2D_V1_R6_FILE_MANIFEST_SHA256.txt SHA256 761b833e0518bf19152f4124fc72a60c5222fdcfed96d373b9a166293acf443e
BASE Reports/HSB_2D_V1_R5_FILE_MANIFEST_SHA256.txt
1: 18d9922ce7c3c572966b1782309ac0226a1be34c0122677681fae4d9100447bd  BUILD_INFO.md
2: 5878b084fa55167b8398e6905d00537204dcc52b803cd6f91b553c729073f338  CHANGELOG_RU.md
3: 6fec1b71d3252faf08b4b4a7cc7ce4dab951bdfb5111dcf6fb1c5e29d22760c3  Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md
4: f1682cad6656c5b3f4ac885796c6fd8704e4c6f1b18312a4bdb823343dcaacbc  Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md
5: af65b52f24a417b3301bd9a060da6c6b5a658570c69b9fcee14360ce21a6878a  Docs/22_OPEN_DECISIONS_REGISTER_RU.md
6: @BASE_LINE(6)
7: @BASE_LINE(7)
8: @BASE_LINE(8)
9: @BASE_LINE(9)
10: @BASE_LINE(10)
11: @BASE_LINE(11)
12: @BASE_LINE(12)
13: 50a99c6c9078559f3f372172dca2d00ceda4678b0be33c063366719b0f0b25e7  Docs/HSB_2E_API_CONTRACTS_RU.md
14: 1f83ff02976536f578bfb24bb6595d5a8f95da3dfb5cc9154c34094a0634114f  Docs/HSB_2E_BIG_HARVEST_IMPLEMENTATION_CONTRACT_RU.md
15: @BASE_LINE(13)
16: 135d74f654548e4151b5122361ab70adf20cd76e59a70684179625793247fe39  Docs/HSB_2E_FINAL_CLOSE_IMPLEMENTATION_CONTRACT_RU.md
17: c894c6c2a45ba9ab2248b0936eb656760d1304fe306d370c88a8154523ee0597  Docs/HSB_2E_FSM_TRANSITION_TABLE_RU.md
18: @BASE_LINE(14)
19: 5246ab579ec6285f61a4c88dbd7c82a0cc158b02ac6b6000bdf2931dadc4c935  Docs/HSB_2E_INITIAL_LOCK_IMPLEMENTATION_CONTRACT_RU.md
20: 329de96231154156e9dae9cc4b1f6063deb437a2d90844b07d796d81e6d2dc06  Docs/HSB_2E_NEW_FAR_CATCH_UP_IMPLEMENTATION_CONTRACT_RU.md
21: 088ad04200618807c7075e16d1bd73de904df2e76eb2175447715001c39bbe67  Docs/HSB_2E_PARTIAL_FAR_RESERVE_IMPLEMENTATION_CONTRACT_RU.md
22: 8fa551b9c48538568698a37a3bb4d603a7c39b42b60c5f6631d533b95c2db450  Docs/HSB_2E_PERSISTENCE_SCHEMA_RU.md
23: 07e5308e78cf6b2b34f3b158450e24d58558b1be731a453f93ca93b31fd57c6a  Docs/HSB_2E_PRODUCTION_FILE_MAP_RU.md
24: @BASE_LINE(16)
25: 5c173756bb7e29f7c4642acc78869da976078a6909b1be88185204ca032df854  Docs/HSB_2E_SMALL_TRANSITION_IMPLEMENTATION_CONTRACT_RU.md
26: @BASE_LINE(17)
27: f214f91f65b664a2f368f96dfc3dc725d3dbb2e645ced88642253543092b033c  Docs/HSB_2E_TRANSACTION_LIFECYCLE_RU.md
28: @BASE_LINE(18)
29: @BASE_LINE(19)
30: @BASE_LINE(20)
31: @BASE_LINE(21)
32: @BASE_LINE(22)
33: @BASE_LINE(23)
34: @BASE_LINE(24)
35: @BASE_LINE(25)
36: @BASE_LINE(26)
37: @BASE_LINE(27)
38: @BASE_LINE(28)
39: @BASE_LINE(29)
40: @BASE_LINE(30)
41: @BASE_LINE(31)
42: @BASE_LINE(32)
43: @BASE_LINE(33)
44: @BASE_LINE(34)
45: @BASE_LINE(35)
46: @BASE_LINE(36)
47: @BASE_LINE(37)
48: @BASE_LINE(38)
49: @BASE_LINE(39)
50: @BASE_LINE(40)
51: @BASE_LINE(41)
52: @BASE_LINE(42)
53: @BASE_LINE(43)
54: @BASE_LINE(44)
55: @BASE_LINE(45)
56: @BASE_LINE(46)
57: @BASE_LINE(47)
58: @BASE_LINE(48)
59: @BASE_LINE(49)
60: @BASE_LINE(50)
61: @BASE_LINE(51)
62: @BASE_LINE(52)
63: @BASE_LINE(53)
64: @BASE_LINE(54)
65: @BASE_LINE(55)
66: @BASE_LINE(56)
67: @BASE_LINE(57)
68: @BASE_LINE(58)
69: @BASE_LINE(59)
70: @BASE_LINE(60)
71: @BASE_LINE(61)
72: @BASE_LINE(62)
73: @BASE_LINE(63)
74: @BASE_LINE(64)
75: @BASE_LINE(65)
76: @BASE_LINE(66)
77: @BASE_LINE(67)
78: @BASE_LINE(68)
79: @BASE_LINE(69)
80: @BASE_LINE(70)
81: @BASE_LINE(71)
82: @BASE_LINE(72)
83: @BASE_LINE(73)
84: @BASE_LINE(74)
85: @BASE_LINE(75)
86: @BASE_LINE(76)
87: @BASE_LINE(77)
88: @BASE_LINE(78)
89: @BASE_LINE(79)
90: @BASE_LINE(80)
91: @BASE_LINE(81)
92: @BASE_LINE(82)
93: @BASE_LINE(83)
94: @BASE_LINE(84)
95: @BASE_LINE(85)
96: @BASE_LINE(86)
97: @BASE_LINE(87)
98: @BASE_LINE(88)
99: @BASE_LINE(89)
100: @BASE_LINE(90)
101: @BASE_LINE(91)
102: f0fb099d164116860b5ea0c15edbad6ee337de3f0fae5e709fb49a2229975bdc  PROJECT_MAP_RU.md
103: c119e6dce1d72e9d1c19df0bbda93ecfb9981e6de274a91d325757c267bb9886  README_RU.md
104: 1a3f321d16d282db8e2bd6202abc69b2fa923bced39b89fd15c35b03db9b8850  Reports/HSB_2D_V1_R6_FALSE_PASS_ANALYSIS_RU.md
105: c683269ad3f6d6c31400c7618163ab631e71c608052b3edfa4e0a07463039d1c  Reports/HSB_2D_V1_R6_FINAL_VERDICT_RU.md
106: 8e39fb598f08c03c656777ab952b701d644077e1576e8505be6fba38db545bbc  Reports/HSB_2D_V1_R6_MUTATION_AUDIT_RU.md
107: bbd546cb6ff2928461a93e1e220f839c9f6608102d0c839b902e20ea6f5b1497  Reports/HSB_2D_V1_R6_REOPENING_RU.md
108: @BASE_LINE(98)
109: e1089e337cd28f6205a1e318607d5ced619db86d53d5ef85988be7131299904c  Reports/HSB_2E_PREP_R1_COMPLETENESS_AUDIT_RU.md
110: 1d74b237535986bf576f21ffe9a8f607dbeb34723eb93403ae4b3c29f2635c04  Reports/HSB_2E_PREP_R1_GAP_ANALYSIS_RU.md
111: @BASE_LINE(99)
112: @BASE_LINE(100)
113: 370ccb3e02bcbbdabc88b4bfa2a43aa59fd997a88d5e5bfc047b3994500b2051  Tests/Static/hsb_2d_v1_r6_mutations.json
114: 16ac1dd4ff01105fbd5760c23b7248463e7e2d9fa95ddd8d3e58adda631fc635  Tests/Static/hsb_2e_api_contracts.json
115: @BASE_LINE(102)
116: 23177b5b2e69f563aee51aa275110a0f560b68041ef14577823cf242593a851b  Tests/Static/hsb_2e_fixtures.json
117: db9585dcc6f93841861911bb357965b05691ae447b79df85af589f7deb5e013c  Tests/Static/hsb_2e_fsm_transitions.json
118: 568da334f3583302f7d0ae1450f188ecc3c9a1bf54605e86b7873361884d5158  Tests/Static/hsb_2e_global_invariants.json
119: 5bc40fc420adfbcb8263b7c1ff8c50771e44ff8fc5b09b03407907aa4d1c8021  Tests/Static/hsb_2e_persistence_schema.json
120: 2b88a925d0259d30a4df82dfb579768755a77a6878a1fe204f4d924b000cb833  Tests/Static/hsb_2e_production_file_map.json
121: 3c71ef6f34df011a50ef89aa2ea63d303cfe81dcc3f05de05c19b15565f5a112  Tests/Static/hsb_2e_test_plan.json
122: 28cc8ad0cf5f310cef2501e5fd95eb1b18dcc75361f406cb8e75eac47f0e1012  Tests/Static/hsb_2e_transaction_lifecycle.json
123: 34d9153e3b28182fcd0bf5f31194f13fb246b108a693ad542421f0f65b8ea662  Tests/Static/hsb_mql5_lexer.py
124: d4240253009cbd92197d4b1134ec402085c0076c13cc3f19b9b90b335b8adebd  Tests/Static/run_hsb_2d_v1_r6_mutations.py
125: 7cee9ff9c0786039f042ef20b302322168ee822f8ff9ee90d5ad6513592b13a9  Tests/Static/verify_hsb_2d_v1_r6.py
126: 538326a5cb37f0824263c621dcaf61149036ddcc50c5bfae081bb1b3ee0eedbb  Tests/Static/verify_hsb_2d_v2_user_evidence.py
127: ab3d7394a229b518e3dbb7b303c3b2ab940dba57f725228bbd2f44443056dc6a  Tests/Static/verify_hsb_2e_prep_r1.py

````

### Manifest R7

````text
FILE Reports/HSB_2D_V1_R7_FILE_MANIFEST_SHA256.txt SHA256 cb7550478c2fbb0a6ef17c5765da11350854e1b133b3466e69fcac2fd40e9bd4
BASE Reports/HSB_2D_V1_R6_FILE_MANIFEST_SHA256.txt
1: cce1e4e848cce7f6ba7a73e13d1695e0609a43d35fab86a32c82c3be7c9ba25c  BUILD_INFO.md
2: cb5982613c50f7b18410a656b728715f13153513d70d9090d9a41f276612acd2  CHANGELOG_RU.md
3: 0b3b1699115e68327fafd1fa303bfcd4042c723c256ffef1cfe4dbc56c326228  Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md
4: a68ad50af87ef38b407a442d0587f9cbeaed8cf75f380f324797f308b44e2506  Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md
5: 078e99d1232db0d50b0ae55c5eb589841d3530c333dbf1e83b1d609af2fd14e0  Docs/22_OPEN_DECISIONS_REGISTER_RU.md
6: @BASE_LINE(6)
7: @BASE_LINE(7)
8: @BASE_LINE(8)
9: @BASE_LINE(9)
10: @BASE_LINE(10)
11: @BASE_LINE(11)
12: @BASE_LINE(12)
13: a71ffd89481382fa584debf48f8a2743bf34eb7349b30e886cc3f1fabcc1aa55  Docs/HSB_2E_API_CONTRACTS_R2_RU.md
14: @BASE_LINE(13)
15: @BASE_LINE(14)
16: @BASE_LINE(15)
17: @BASE_LINE(16)
18: 753ebaa8f50339908f6bfdf3a1b4276050a642e56e711216e84e222eaedbf0bb  Docs/HSB_2E_FORMULA_CONTRACTS_R2_RU.md
19: @BASE_LINE(17)
20: @BASE_LINE(18)
21: @BASE_LINE(19)
22: @BASE_LINE(20)
23: @BASE_LINE(21)
24: @BASE_LINE(22)
25: 7958e7ab05473e8c8bc001717a8914933c1c9bf4e909ecb0cd840b998115db4b  Docs/HSB_2E_PREP_R2_ADMIN_HANDOFF_RU.md
26: @BASE_LINE(23)
27: a6ccfb8f722ec2d050a7cfaab47db3cf95e7d8be72f4aa741643ed5634923d2d  Docs/HSB_2E_SCENARIO_CONTRACTS_R2_RU.md
28: @BASE_LINE(24)
29: @BASE_LINE(25)
30: @BASE_LINE(26)
31: @BASE_LINE(27)
32: @BASE_LINE(28)
33: @BASE_LINE(29)
34: @BASE_LINE(30)
35: @BASE_LINE(31)
36: @BASE_LINE(32)
37: @BASE_LINE(33)
38: @BASE_LINE(34)
39: @BASE_LINE(35)
40: @BASE_LINE(36)
41: @BASE_LINE(37)
42: @BASE_LINE(38)
43: @BASE_LINE(39)
44: @BASE_LINE(40)
45: @BASE_LINE(41)
46: @BASE_LINE(42)
47: @BASE_LINE(43)
48: @BASE_LINE(44)
49: @BASE_LINE(45)
50: @BASE_LINE(46)
51: @BASE_LINE(47)
52: @BASE_LINE(48)
53: @BASE_LINE(49)
54: @BASE_LINE(50)
55: @BASE_LINE(51)
56: @BASE_LINE(52)
57: @BASE_LINE(53)
58: @BASE_LINE(54)
59: @BASE_LINE(55)
60: @BASE_LINE(56)
61: @BASE_LINE(57)
62: @BASE_LINE(58)
63: @BASE_LINE(59)
64: @BASE_LINE(60)
65: @BASE_LINE(61)
66: @BASE_LINE(62)
67: @BASE_LINE(63)
68: @BASE_LINE(64)
69: @BASE_LINE(65)
70: @BASE_LINE(66)
71: @BASE_LINE(67)
72: @BASE_LINE(68)
73: @BASE_LINE(69)
74: @BASE_LINE(70)
75: @BASE_LINE(71)
76: @BASE_LINE(72)
77: @BASE_LINE(73)
78: @BASE_LINE(74)
79: @BASE_LINE(75)
80: @BASE_LINE(76)
81: @BASE_LINE(77)
82: @BASE_LINE(78)
83: @BASE_LINE(79)
84: @BASE_LINE(80)
85: @BASE_LINE(81)
86: @BASE_LINE(82)
87: @BASE_LINE(83)
88: @BASE_LINE(84)
89: @BASE_LINE(85)
90: @BASE_LINE(86)
91: @BASE_LINE(87)
92: @BASE_LINE(88)
93: @BASE_LINE(89)
94: @BASE_LINE(90)
95: @BASE_LINE(91)
96: @BASE_LINE(92)
97: @BASE_LINE(93)
98: @BASE_LINE(94)
99: @BASE_LINE(95)
100: @BASE_LINE(96)
101: @BASE_LINE(97)
102: @BASE_LINE(98)
103: @BASE_LINE(99)
104: @BASE_LINE(100)
105: @BASE_LINE(101)
106: b81aa8fe3ce9be6fcb99fa6b3cc6932f86d4d65b2533d3e059cf70c73a166950  PROJECT_MAP_RU.md
107: 6ade49b15137d61f787d319ff1c09a533bb9af5a20ded590059bbfaa1fe13a7f  README_RU.md
108: c21b911bada5b92df4fbb1d65c7031b13f329abeb0fc91de9abb1c46e76c82ff  Reports/HSB_2D_V1_R7_FALSE_PASS_ANALYSIS_RU.md
109: dad67ad14d50d1f2300a820dd7651d5312f8960d8033d465016c5bed8c2a0160  Reports/HSB_2D_V1_R7_FINAL_VERDICT_RU.md
110: 839fc96a78fc56b5a44021279ab8589eb8bc32d6891a1660c99bda6888214828  Reports/HSB_2D_V1_R7_MUTATION_AUDIT_RU.md
111: @BASE_LINE(108)
112: @BASE_LINE(109)
113: @BASE_LINE(110)
114: 9aa1c95eb9dda57c5fd6297ba01536d39231712a10d818ca47005d0805f02c1a  Reports/HSB_2E_PREP_R2_COMPLETENESS_AUDIT_RU.md
115: 90e67d25d5687ebbb4794874faafd355b96d25dd2247624e8b49d01c3b4fd1c1  Reports/HSB_2E_PREP_R2_SEMANTIC_AUDIT_RU.md
116: @BASE_LINE(111)
117: @BASE_LINE(112)
118: 41a06bd630105b4c92a1aee2a7f3dfc31c09c295e446400c4f7a7e2b00ab875b  Tests/Static/hsb_2d_v1_r7_mutations.json
119: @BASE_LINE(114)
120: 9fe819c874502f70c90edba503ae86af8871f8f3cf044c90ddd4d826e4ed56a2  Tests/Static/hsb_2e_api_contracts_r2.json
121: @BASE_LINE(115)
122: @BASE_LINE(116)
123: bb0e87b6f9cb67b66f442368836104f353954ce1895651be65d56c6117ac2415  Tests/Static/hsb_2e_fixtures_r2.json
124: 0ce83434f319be727d3604620fc80bba20827bb58b377cf7de736ef0bde75de1  Tests/Static/hsb_2e_formula_contracts_r2.json
125: @BASE_LINE(117)
126: @BASE_LINE(118)
127: @BASE_LINE(119)
128: @BASE_LINE(120)
129: af18236f2f3a3e1f8e148af1e1326f9febd9016c75e9cea277bc9edbdd5d5d2e  Tests/Static/hsb_2e_scenario_contracts_r2.json
130: @BASE_LINE(121)
131: f6281c6e307d5ca4d9c3ad4715faa2c6152bf0b664939a05d126df286762a0dd  Tests/Static/hsb_2e_test_plan_r2.json
132: @BASE_LINE(122)
133: 100ecdcdd510ece397fd6ebbf6b46a16b77cf10bcb445022c6f2233240d4d138  Tests/Static/hsb_mql5_lexer.py
134: 4828ea99cd57a11401d7dceabe9c4d3cf96fb8a84dbc3cb94934e2878e4a5316  Tests/Static/run_hsb_2d_v1_r7_mutations.py
135: 96e801df1ac81fb1a27f5c21a2877345f37391cf18210d738b8a56c1ee55a1c0  Tests/Static/verify_hsb_2d_v1_r7.py
136: @BASE_LINE(126)
137: @BASE_LINE(127)
138: d5c8d9edce9520452d85bcb6aa277eab702fda2eb4ebd531ac769732df520e14  Tests/Static/verify_hsb_2e_prep_r2.py

````
