use('mongodbVSCodePlaygroundDB');

// Query 1

db.classroom.aggregate([
{
  $lookup: {
    from: "section",
    localField: "room_number",
    foreignField: "room_number",
    as: "sections"
  }
},
{
  $unwind: "$sections"
},
{
  $lookup: {
    from: "teaches",
    localField: "sections.course_id",
    foreignField: "course_id",
    as: "teaches"
  }
},
{
  $unwind: "$teaches"
},
{
  $lookup: {
    from: "instructor",
    localField: "teaches.id",
    foreignField: "id",
    as: "instructors"
  }
},
{
  $unwind: "$instructors"
},
{
  $project: {
    _id: 0,
    name: "$instructors.name",
    building: "$building",
    room_number: "$room_number"
  }
},
{
  $group: {
    _id: {
      name: "$name",
      building: "$building",
      room_number: "$room_number"
    }
  }
},
{
  $project: {
    _id: 0,
    name: "$_id.name",
    building: "$_id.building",
    room_number: "$_id.room_number"
  }
}
])

// Query 2

db.student.aggregate([
    {
        $lookup: {
            from: "advisor",
            localField: "ID",
            foreignField: "s_ID",
            as: "advisor"
        }
    },
    {
        $unwind: "$advisor"
    },
    {
        $lookup: {
            from: "instructor",
            localField: "advisor.i_ID",
            foreignField: "ID",
            as: "instructor"
        }
    },
    {
        $unwind: "$instructor"
    },
    {
        $lookup: {
            from: "takes",
            localField: "instructor.ID",
            foreignField: "ID",
            as: "takes"
        }
    },
    {
        $unwind: "$takes"
    },
    {
        $lookup: {
            from: "course",
            localField: "takes.course_id",
            foreignField: "course_id",
            as: "course"
        }
    },
    {
        $unwind: "$course"
    },
    {
        $project: {
            "Estudante": "$name",
            "Instrutor": "$instructor.name",
            "Disciplina": "$course.title"
        }
    }
]);

// Query 3

db.department.aggregate([
  {
    $lookup: {
      from: "student",
      localField: "dept_name",
      foreignField: "dept_name",
      as: "students"
    }
  },
  {
    $unwind: {
      path: "$students",
      preserveNullAndEmptyArrays: true
    }
  },
  {
    $lookup: {
      from: "instructor",
      localField: "dept_name",
      foreignField: "dept_name",
      as: "instructors"
    }
  },
  {
    $unwind: {
      path: "$instructors",
      preserveNullAndEmptyArrays: true
    }
  },
  {
    $group: {
      _id: "$dept_name",
      budget: { $first: "$budget" },
      studentCount: { $sum: 1 },
      averageSalary: { $avg: "$instructors.salary" }
    }
  },
  {
    $project: {
      _id: 0,
      dept_name: "$_id",
      budget: 1,
      studentCount: 1,
      averageSalary: 1
    }
  }
])
