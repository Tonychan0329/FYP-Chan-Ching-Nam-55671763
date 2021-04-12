-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 12, 2021 at 11:49 AM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `FYP_booking`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(8) NOT NULL,
  `admin_email` varchar(100) NOT NULL,
  `admin_password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_email`, `admin_password`) VALUES
(1, 'admin@gmail.com', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cart_id` int(8) NOT NULL,
  `username` varchar(100) NOT NULL,
  `product_id` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

CREATE TABLE `message` (
  `mes_id` int(8) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `subject` text DEFAULT NULL,
  `mes_body` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `message`
--

INSERT INTO `message` (`mes_id`, `name`, `email`, `subject`, `mes_body`) VALUES
(1, 'tony', 'tony@gmail.com', 'hello', 'bye'),
(2, 'tonychan', 'tonychan', 'hello', 'heoll'),
(3, 'tony', 'Tchan@gmail.com', 'heloo', 'heloo'),
(4, 'chan', 'yhlcadcmjjuo@maxresistance.com', 'hello', 'helooo');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(8) NOT NULL,
  `username` varchar(100) NOT NULL,
  `dates` date NOT NULL,
  `totalprice` varchar(100) NOT NULL,
  `status` varchar(100) DEFAULT NULL,
  `shipping_status` varchar(100) NOT NULL DEFAULT 'Ready To Ship'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `username`, `dates`, `totalprice`, `status`, `shipping_status`) VALUES
(13, 'tonychan', '2021-03-26', '147', 'Payment Completed', 'Ready To Ship'),
(16, 'tonychan123', '2021-03-28', '88', 'Payment Completed', 'Arrived'),
(18, 'tonychan', '2021-03-28', '25', 'Payment Completed', 'Ready To Ship'),
(19, 'tony1245', '2021-03-29', '88', 'Payment Completed', 'Arrived'),
(23, 'tonychan', '2021-04-04', '25', 'Payment Completed', 'Ready To Ship');

-- --------------------------------------------------------

--
-- Table structure for table `order_detail`
--

CREATE TABLE `order_detail` (
  `od_id` int(8) NOT NULL,
  `order_id` int(8) DEFAULT NULL,
  `product_id` int(8) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `order_detail`
--

INSERT INTO `order_detail` (`od_id`, `order_id`, `product_id`, `username`, `status`) VALUES
(17, 13, 13, 'tonychan', 'Payment Completed'),
(18, 13, 15, 'tonychan', 'Payment Completed'),
(23, 16, 15, 'tonychan123', 'Payment Completed'),
(25, 18, 16, 'tonychan', 'Payment Completed'),
(26, 19, 15, 'tony1245', 'Payment Completed'),
(28, 23, 16, 'tonychan', 'Payment Completed');

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `pay_id` int(8) NOT NULL,
  `card_holder` varchar(100) DEFAULT NULL,
  `ccv` varbinary(100) DEFAULT NULL,
  `c_no` varbinary(100) DEFAULT NULL,
  `totalprice` varchar(100) DEFAULT NULL,
  `order_id` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`pay_id`, `card_holder`, `ccv`, `c_no`, `totalprice`, `order_id`) VALUES
(5, 'Tonychan', 0xa547ec366da43b9e8470be49bc6aac0a, 0x00a58c99a96f8d46e3a52659321a212d4c97a84d1fee0fc5866b5748e6d06351, '147', 13),
(8, 'tonychan', 0x30c7900b984d01f86225cfd913bf8686, 0x50af6b1c1ba8e0ca7c3b3fd8235132f24c97a84d1fee0fc5866b5748e6d06351, '88', 16),
(9, 'tonychan', 0xa547ec366da43b9e8470be49bc6aac0a, 0x00a58c99a96f8d46e3a52659321a212d4c97a84d1fee0fc5866b5748e6d06351, '25', 18),
(10, 'tonychan', 0xa547ec366da43b9e8470be49bc6aac0a, 0x50af6b1c1ba8e0ca7c3b3fd8235132f24c97a84d1fee0fc5866b5748e6d06351, '88', 19),
(12, 'Tonychan', 0xa547ec366da43b9e8470be49bc6aac0a, 0xff0c189be8cfe6ca63fd7df7261300b54c97a84d1fee0fc5866b5748e6d06351, '25', 23);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `product_id` int(8) NOT NULL,
  `name` varchar(255) NOT NULL,
  `image` text NOT NULL,
  `price` double NOT NULL,
  `stock` varchar(100) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`product_id`, `name`, `image`, `price`, `stock`, `description`, `status`) VALUES
(1, 'Mask KF94', 'product1.jpg', 25, '500', 'The effect of blocking droplet infection is 99.9%! Bacterial filtration efficiency is higher than 94%!', 'SOLD OUT'),
(3, 'Alcohol Wet Wipes', 'product3.jpg', 200, '100', 'wipe down whatever surface you would like to clean ~at least 60% alcohol', 'ON SALE'),
(4, 'Hand Sanitizr', 'product4.jpg', 25, '60', 'No washing,quick drying,easy to use,mild hand protection', 'ON SALE'),
(5, 'Rubbing Alcohol 50ml/2', 'product5.jpg', 40, '100', '70% First Aid Antiseptic at Walgreens', 'ON SALE'),
(13, 'san hao rice', 'product-2.jpeg', 59.9, '100', 'tainun #71(2kg) from Taiwan', 'ON SALE'),
(15, 'peanut oil 3s', 'product-3.jpeg', 88, '100', 'peanut oil 3s(900ml) from Hong Kong Contains peanuts and/or soy', 'ON SALE'),
(16, 'mini wafer tray /p', 'product-4.jpeg', 25, '100', 'garden mini wafer tray /p(272gm)', 'ON SALE'),
(17, 'swanson chicken broth', 'product-5.jpeg', 16.9, '100', 'chicken broth(1lt) Contains peanuts and/or soy, Contains milk', 'ON SALE'),
(18, 'coca cola', 'product-6.jpeg', 33.5, '100', 'coke can 8s(330ml) from Hong Kong', 'ON SALE'),
(19, 'Mask KF94', 'product2.jpg', 300, '200', 'BFE 99%, VFE 99%, PFE 99%', 'SOLD OUT');

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--

CREATE TABLE `reservation` (
  `reser_id` int(8) NOT NULL,
  `service_id` int(8) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `fullname` varchar(100) NOT NULL,
  `service_name` varchar(255) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `reservation`
--

INSERT INTO `reservation` (`reser_id`, `service_id`, `email`, `username`, `fullname`, `service_name`, `address`, `phone`, `date`, `time`) VALUES
(9, 1, 'yhlcadcmjjuo@maxresistance.com', 'tonychan123', 'TonyChan', 'MEDICAL / 醫療', 'City Univerity of Hong Kong, Kowloon Tong, Kowloon, HK', '23323202', '2021-03-30', '17:03:00'),
(10, 1, 'yosoni5964@asfalio.com', 'tony1245', 'tonychan', 'MEDICAL / 醫療', 'City Univerity of Hong Kong, Kowloon Tong, Kowloon, HK', '23323202', '2021-04-01', '10:08:00'),
(13, 2, 'yosoni5964@asfalio.com', 'tonychan', 'Ching NamChan', 'MEDICAL EXAM / 身體檢查', 'City Univerity of Hong Kong, Kowloon Tong, Kowloon, HK', '98635622', '2021-04-12', '16:25:00');

-- --------------------------------------------------------

--
-- Table structure for table `service`
--

CREATE TABLE `service` (
  `service_id` int(8) NOT NULL,
  `service_name` varchar(225) NOT NULL,
  `service_image` text NOT NULL,
  `description` text NOT NULL,
  `service_detail` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `service`
--

INSERT INTO `service` (`service_id`, `service_name`, `service_image`, `description`, `service_detail`) VALUES
(1, 'MEDICAL / 醫療', 'M-A.png', '\"Medical\"- This service will provide outpatient treatment by professional doctors or nurses, and provide simple diagnosis and treatment services and general outpatient treatments for the elderly in need or mobility issues, such as colds, flus, fevers, etc. / 此服務將會專業的醫生或護士提供上門診治, 為有需要或行動不便長者提供簡單的診治服務和普遍的門診治療，例如傷風、感冒、發燒等。', 'The details of the charges are as follows: HK$320 per visit (including three days of medicine)/ 收費詳情如下: 每次上門收費港幣320元(包括3日的藥費)'),
(2, 'MEDICAL EXAM / 身體檢查', 'medical-report.png', '\"Medical Exam\" - This service will provide on-site physical examinations by professional doctors or nurses, and provide simple examination services for the elderly in need and mobility, such as blood pressure measurement, blood sugar test, and simple physical examination to ensure that they are in good health. / 此服務將會專業的醫生或護士提供上門身體檢查, 為有需要和行動不便的長者提供簡單的檢查服務，例如量度血壓、驗血糖、簡單的身體檢查，以確保他們的身體狀況良好。', 'The details of the charges are as follows: HK$200 per visit / 收費詳情如下: 每次上門收費港幣200元'),
(3, 'PHYSIOTHERAPY / 物理治療', 'phy.png', 'The physical therapist visits the patient home for examination, training, treatment and evaluation. Physiotherapists also bring portable treatment equipment and training equipment to provide appropriate home physiotherapy services. Basic service scope: follow-up after surgery for bedridden patients, chest and lung treatment and assessment, pain and trauma treatment, physical training, daily activity training. / 物理治療師親臨病患者家中，進行檢查、訓練、治療及評估。物理治療師亦帶備可攜式治療器材及訓練用具，提供適切的家居物理治療服務。基本服務範圍：臥床病者手術後跟進、胸肺科治療及評估、痛症及創傷治療、體能訓練、日常活動訓練。', 'Each session takes about 45 minutes, depending on the complexity and needs of the disease. The charge is HK$400 per session/ 每節治療約45分鐘，視乎病症的複雜性及需要而定。收費為每一節港幣$400'),
(4, 'PERSONAL ASSISTANCE / 個人照顧', 'P-A.png', 'A team of occupational therapists, nurses, social workers, speech therapists, dietitians, rehabilitation assistants and care assistants will make detailed assessments based on users physical and mental conditions and environmental factors, and then integrate the most suitable care packages for users. Personal care: personal hygiene (assisting in bathing, shampooing, incontinence treatment, etc.), feeding, and assisting in handling personal affairs (accompanying outing, accompany doctors, accompanying conversations, etc.), meal arrangements: purchasing ingredients, preparing and cooking meals. / 由職業治療師、護士、社工、言語治療師、營養師、復康助理及照顧助理團隊，因應用戶的身心狀況及環境因素等作詳盡評估，繼而整合最合適用戶的照顧配套。起居照顧：個人衞生(協助洗澡、洗髮、失禁處理等)、餵食，以及協助處理個人事務(陪伴外出、陪診、陪伴交談等)、 膳食安排：代購食材、預備及烹調膳食。', 'The details of the charges are as follows: HK$475/ the first 2 hours, thereafter hourly charge: HK$65 / 收費詳情如下: HK$475/ 首2小時，其後每小時收費：HK$65'),
(5, 'NUTRITION / 營養配搭', 'nutrition-2.png', 'Provide professional nutrition consultation and diet treatment services for diabetes, high cholesterol, hypertension, kidney disease, cancer, liver disease, gout, anemia, constipation, irritable bowel syndrome, malnutrition, elderly nutrition, chronic obstructive pneumonia and other diseases. In addition, the elders in need prepare a menu, and prepare food according to the content of the menu to deliver to the elderly’s home. / 為糖尿病丶高膽固醇丶高血壓丶腎病丶癌症丶肝病丶痛風症丶貧血丶便秘丶腸易激綜合症丶營養不良丶老人營養丶慢性阻塞性肺炎等病症提供專業的營養諮詢及飲食治療服務。另外有需要的長者準備餐單，根據餐單內容準備食物送到長者家中。', 'The details of the charges are as follows: Each elder HK$3600 per month / 有關收費的詳情如下：每位長者每個月為港幣$ 3600'),
(6, 'COGNITIVE ACTIVITIES / 認知訓練', 'brain.png', 'Special personnel will first come to assess the status of the elders and formulate an effective training plan, and then trainers will come to the door regularly to provide training for the elders to delay the rate of decline. Service content: \"Life-oriented training: mainly through games and exercises, training cognitive ability and daily self-care ability, providing reality orientation, nostalgia therapy, rehabilitation training, speech therapy, etc. Home improvement suggestions: inspect the living environment of the elderly and provide suggestions for improvement, such as adding environmental reminders to reduce the chance of confusion for the elderly. Caregiver support: door-to-door teaching caregivers use appropriate teaching materials and daily necessities to train the elderly. Case management: conduct regular assessments, follow up the situation of the elderly, and provide follow-up, referral, counseling, caregiver support, etc. when necessary. \" / 專人首先會上門評估長者的狀態和制定有效的訓練計劃，之後訓練員會定期上門，為長者提供訓練，延緩衰退的速度。服務內容：「生活化訓練：主要透過遊戲及練習，訓練認知能力和日常自理能力﹑提供現實導向﹑懷緬治療﹑復康訓練﹑言語治療等。 改善家居建議：視察長者的居住環境，提供改善建議，例如加入環境提示，減少長者產生混亂的機會。 照顧者支援：上門教導照顧者使用合適教材和生活物品為長者訓練。 個案管理：作定期評估，跟進長者的狀況，有需要時提供跟進﹑轉介﹑輔導﹑照顧者支援等。」', 'The details of the charges are as follows: HK$200 per visit / 收費詳情如下: 每次上門收費港幣200元'),
(9, 'HOUSE KEEPING / 家居清潔', 'housekeeping.png', 'Standard services include basic tasks such as cleaning rooms, living rooms, toilets, bathrooms, kitchens, windows and doors, furniture throughout the house, mopping the floor, changing sheets and quilts, buying food in the market, washing and ironing clothes (excluding hand laundry). / 標準服務範圍包括清潔房間、客廳、洗手間、浴室、廚房、窗門、全屋傢俱、拖地、更換床單被舖、街市買餸、洗熨衣物 (不包括手洗衣物) 等基本工作。', 'The details of the charges are as follows: HK$80 per hour / 有關收費的詳情如下：每小時港幣80元'),
(10, 'LAUNDRY / 送洗衣服', 'laundry.png', 'Provide laundry, dry cleaning, and home delivery services for the elderly / 為長者提供洗衣、乾洗、上門收送的服務', 'Wash & Fold $6/lbs $ 60 /10 lbs, after $5/lbs , 2 days turnaround, Free delivery service, Minimum Charge $80 / 磅洗 $6/磅 首$ 60 / 10磅, 其後$5/磅  只需2天即可送回乾淨衣物  免費上門收送服務  最低消費 $800'),
(11, 'HOUSE REPAIR / 家居維修', 'repair.png', 'Home repair project service content: including home repairs of large and small water and electricity, such as lamp repair, TV repair, refrigerator repair, plumbing faucet, whole induction cooker, stove inspection and repair, etc. / 家居維修項目服務內容：包括家中大大小小水電維修，例如電燈維修、電視維修、雪櫃維修、整水喉水龍頭、整電磁爐、爐具檢查維修等。', 'The details of the charges are as follows: HK$100 per repair / 收費詳情如下: 每項維修HK$100'),
(12, 'COUNSELING / 心理輔導', 'counseling.png', 'A multi-professional team composed of social workers, nurses and physiotherapists assists elders who are 60 years of age or older who suffer from emotional distress/depression symptoms or who have been referred by the hospital or geriatric psychiatric department. Plan or rebuild a healthy lifestyle for them, improve their positive emotions and self-management skills, and rebuild their self-confidence. / 由社工、護士及物理治療師組成跨專業團隊，協助60 歲或以上的長者患有情緒困擾/ 出現抑鬱徵狀或由醫院或老人精神科轉介之離院長者。為他們規劃或重建健康生活模式、提升正面情緒及自我管理能力、重建自信。', 'The details of the charges are as follows: HK$100 per visit / 收費詳情如下: 每次收費港幣100元');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(8) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `FirstName` varchar(20) DEFAULT NULL,
  `LastName` varchar(20) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `FirstName`, `LastName`, `phone`, `address`, `gender`) VALUES
(12, 'tonychan', '1234', 'yosoni5964@asfalio.com', 'Ching Nam', 'Chan', '98635622', 'City Univerity of Hong Kong, Kowloon Tong, Kowloon, HK', 'Male'),
(15, 'tonychan123', '1234', 'yhlcadcmjjuo@maxresistance.com', 'Tony', 'Chan', '23323202', 'City Univerity of Hong Kong, Kowloon Tong, Kowloon, HK', 'Male'),
(17, 'tonychan134', '123', 'gzvefpsjyfjkc@maxresistance.com', NULL, NULL, NULL, NULL, NULL),
(18, 'tony1245', '1234', 'yosoni5964@asfalio.com', 'tony', 'chan', '23323202', 'City Univerity of Hong Kong, Kowloon Tong, Kowloon, HK', 'Male');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`mes_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `order_detail`
--
ALTER TABLE `order_detail`
  ADD PRIMARY KEY (`od_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`pay_id`),
  ADD KEY `order_id` (`order_id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `reservation`
--
ALTER TABLE `reservation`
  ADD PRIMARY KEY (`reser_id`),
  ADD KEY `service_id` (`service_id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `service`
--
ALTER TABLE `service`
  ADD PRIMARY KEY (`service_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `cart_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `message`
--
ALTER TABLE `message`
  MODIFY `mes_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `order_detail`
--
ALTER TABLE `order_detail`
  MODIFY `od_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `payment`
--
ALTER TABLE `payment`
  MODIFY `pay_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `product_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `reservation`
--
ALTER TABLE `reservation`
  MODIFY `reser_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `service`
--
ALTER TABLE `service`
  MODIFY `service_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `order_detail`
--
ALTER TABLE `order_detail`
  ADD CONSTRAINT `order_detail_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `order_detail_ibfk_3` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`service_id`) REFERENCES `service` (`service_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `reservation_ibfk_2` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
